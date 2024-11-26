import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser

LANGUAGE = Language(tscpp.language())


QUERY = LANGUAGE.query("""
(function_definition 
  declarator: (function_declarator 
                name: (identifier) @fn-name
                parameters: (parameter_list) @params)
  )
""")


global_parser = Parser(LANGUAGE)


def get_fn_name(code, parser=global_parser):
    src = bytes(code, "utf8")
    tree = parser.parse(src)
    node = tree.root_node
    for cap, typ in QUERY.captures(node):
        if typ == "fn-name":
            return node_to_string(src, cap)
    return None


def node_to_string(src: bytes, node):
    return src[node.start_byte:node.end_byte].decode("utf8")


def make_parser():
    _parser = Parser(LANGUAGE)
    return _parser


RETURN_QUERY = LANGUAGE.query("""
(return_statement) @return
""")


def does_have_return(src, parser=global_parser):
    tree = parser.parse(bytes(src, "utf8"))
    root = tree.root_node
    captures = RETURN_QUERY.captures(root)
    for node, _ in captures:
        # if it doesn't have an argument, it's not a return with a value
        if len(node.children) <= 1:  # includes "return" itself
            continue
        else:
            return True

    return False


if __name__ == "__main__":
    code = """
#include <iostream>
using namespace std;
"""
    print(global_parser.parse(bytes(code, "utf8")).root_node)