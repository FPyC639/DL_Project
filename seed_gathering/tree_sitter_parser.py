import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser

LANGUAGE = Language(tscpp.language())


QUERY = LANGUAGE.query("""
(
  (function_definition
    type: (_)                 
    declarator: (
      function_declarator
        declarator: (identifier) @function.name
        parameters: (parameter_list)
    )
    body: (compound_statement) 
  ) @function.def
)
""")


global_parser = Parser(LANGUAGE)


def get_fn_name(code, parser=global_parser):
    buf = bytes(code, "utf8")
    tree = parser.parse(buf)
    captures = QUERY.captures(tree.root_node)
    function_names = captures.get("function.name", [])
    for name in function_names:
        return node_to_string(buf, name)

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
    for capture in captures:
        # if it doesn't have an argument, it's not a return with a value
        if capture == "return":  # includes "return" itself
            return True
        else:
          continue

    return False


if __name__ == "__main__":
    code = """
#include <iostream>
using namespace std;
"""
    print(global_parser.parse(bytes(code, "utf8")).root_node)