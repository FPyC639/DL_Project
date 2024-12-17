from seed_gathering.fetch_code_from_s3 import download_contents
from tree_sitter_parser import LANGUAGE, make_parser, node_to_string
import datasets
import os
import signal
from multiprocessing import Pool

TOPLEVEL_QUERY = LANGUAGE.query("""
(
    (function_definition
        type: (primitive_type)
        declarator: (
            function_declarator
                declarator: (identifier) @function.name
                parameters: (parameter_list)
        )
        body: (compound_statement) @function.body
    ) @function.def
)
""")


def get_top_level_functions(src, tree):
    captures = TOPLEVEL_QUERY.captures(tree.root_node)
    res = []
    # SELECTING FUNCTIONS
    function_nodes = captures.get("function.def", [])

    for node in function_nodes:
        # if the starting col is not 0, then it's not a top-level fn
        _, col = node.start_point
        if col != 0:
            continue
        res.append(node_to_string(src, node))

    return res


def parse_ex(parser, ex):
    ex = download_contents(ex["blob_id"], ex["src_encoding"])
    try:
        buf = bytes(ex, "utf8")
        tree = parser.parse(buf)
        return get_top_level_functions(buf, tree)
    except:
        return []


# if one parser segfaults, we can just make a new one and other parsers will still be fine
# WE LOVE TREE SITTER!
PARSERS = None


def process_chunk(idx_and_chunk):
    assert PARSERS is not None
    idx, chunk = idx_and_chunk
    parser = PARSERS[idx]
    chunk_new_funs = set()
    for ex in chunk:
        chunk_new_funs.update(parse_ex(parser, ex))
    return chunk_new_funs


def main(args):
    global PARSERS
    ds = datasets.load_dataset(
        "bigcode/the-stack-v2-dedup", data_dir="data/C++",
        split='train', streaming=True)
    dataset_head = ds.take(200)
    funs = set()
    PARSERS = [make_parser() for _ in range(args.num_workers)]
    total_len = len(list(dataset_head))
    CHUNK_SIZE = 1000 * args.num_workers

    print(f"Total length: {total_len}")
    print(f"Chunk size: {CHUNK_SIZE}")

    chunk = []
    p = Pool(args.num_workers)
    for i, ex in enumerate(ds):
        if i % (total_len // 100) == 0:
            print(f"{i}/{total_len}")
        try:
            chunk.append(ex)
            if len(chunk) == CHUNK_SIZE or i == total_len - 1:
                print(f"Processing chunk {i // CHUNK_SIZE}")
                # divide the chunk into NUM_WORKERS chunks
                subchunk_size = len(chunk) // args.num_workers
                subchunks = [chunk[i:i + subchunk_size]
                             for i in range(0, len(chunk), subchunk_size)]
                new_funs_iter = p.imap(
                    process_chunk, [(i, subchunk) for i, subchunk in enumerate(subchunks)])
                print("Getting new functions")
                len_before = len(funs)
                while True:
                    try:
                        def timeout_handler(_, __):
                            raise KeyboardInterrupt  # it's fineeeeeee
                        signal.signal(signal.SIGALRM, timeout_handler)
                        signal.alarm(60)
                        funs.update(next(new_funs_iter))
                        signal.alarm(0)
                    except KeyboardInterrupt:
                        signal.alarm(0)
                        print("Keyboard interrupt. Terminating pool")
                        p.terminate()
                        p = Pool(args.num_workers)
                        break
                    except StopIteration:
                        break
                    except Exception as e:
                        print(e)

                signal.alarm(0)

                PARSERS = [make_parser() for _ in range(args.num_workers)]

                print(
                    f"Done processing chunk {i // CHUNK_SIZE}. Got {len(funs) - len_before} new functions")

                chunk = []
        except Exception as e:
            print(e)
            chunk = []

        if i == total_len - 1:
            break

    p.close()

    new_ds_dict = {
        "content": list(funs),
        "id": list(range(len(funs)))
    }

    new_ds = datasets.Dataset.from_dict(new_ds_dict)
    new_ds.push_to_hub(args.push, private=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_workers", type=int, default=os.cpu_count())
    parser.add_argument("--dataset", type=str,
                        default="bigcode/the-stack-dedup")
    parser.add_argument("--data_dir", type=str, default="data/c++")
    parser.add_argument("--push", type=str, required=True)
    args = parser.parse_args()
    main(args)