from __future__ import annotations
from typing import List
from load_java_files import load_java_files
import tree_sitter


class JavaAnalyzer:
    """
    class for analyzing a java file
    """

    def __init__(self, name: str, content: str) -> JavaAnalyzer:
        self.name = name  # the name of the java file
        self.content = content  # the content of the java file
        self.package_name = ""  # the name of package it belongs to
        self.import_file_list: List[
            str
        ] = []  # the list of names of the files it imports
        self.import_package_list: List[
            str
        ] = []  # the list of names of the packages it imports

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

    def analyze(self) -> None:
        """
        analyze the code and extract the information
        """

        def analyze_node(node: tree_sitter.Node):
            """
            analyze one node
            """
            match node.type:
                case "package_declaration":
                    self.package_name = node.named_children[0].text.decode()

                    # print(self.package_name)
                    # for child_node in node.named_children:
                    #     print(" ", child_node.type)
                case "import_declaration":
                    # for child_node in node.named_children:
                    #     print(
                    #         " ",
                    #         node.named_child_count,
                    #         child_node.type,
                    #         child_node.text.decode(),
                    #     )

                    match node.named_child_count:
                        case 1:
                            self.import_file_list.append(
                                node.named_children[0].text.decode()
                            )
                        case 2:
                            self.import_package_list.append(
                                node.named_children[0].text.decode()
                            )
                        case _:
                            raise Exception("unhandled situation in import_declaration!")
                    

        for node in self.root_node.named_children:
            print(node.type)
            analyze_node(node)


# test code
if __name__ == "__main__":
    # name_content_list = load_java_files("course-02242-examples")
    name_content_list = load_java_files("example-dependency-graphs")
    java_analyzer_list: list[JavaAnalyzer] = []
    for name, content in name_content_list:
        java_analyzer_list.append(JavaAnalyzer(name, content))

    test_java_analyzer = java_analyzer_list[0]
    test_java_analyzer.analyze()
    print(test_java_analyzer.import_file_list)
    print(test_java_analyzer.import_package_list)
