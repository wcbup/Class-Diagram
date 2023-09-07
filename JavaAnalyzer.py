from __future__ import annotations
from load_java_files import load_java_files
import tree_sitter


class JavaAnalyzer:
    """
    class for analyzing a java file
    """

    def __init__(self, name: str, content: str) -> JavaAnalyzer:
        self.name = name  # the name of the java file
        self.content = content  # the content of the java file

        # load the tree sitter
        tree_sitter.Language.build_library(
            # Store the library in the `build` directory
            "build/my-languages.so",
            # Include one or more languages
            [
                "./tree-sitter-java",
            ],
        )

        # init the parser
        JAVA_LANGUAGE = tree_sitter.Language("build/my-languages.so", "java")
        parser = tree_sitter.Parser()
        parser.set_language(JAVA_LANGUAGE)

        # init the root node
        self.root_node = parser.parse(bytes(self.content, "utf-8")).root_node


# test code
if __name__ == "__main__":
    name_content_list = load_java_files("example-dependency-graphs")
    java_analyzer_list: list[JavaAnalyzer] = []
    for name, content in name_content_list:
        java_analyzer_list.append(JavaAnalyzer(name, content))

    for java_analyzer in java_analyzer_list:
        print(java_analyzer.root_node.text.decode())
