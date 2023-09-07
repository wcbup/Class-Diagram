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
        self.public_class_list: List[str] = []  # the list of public classes it creates

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
                    # scoped_identifier
                    scoped_id_node = node.named_children[0]
                    if scoped_id_node.type != "scoped_identifier":
                        raise Exception("unhandled situation in package_declaration")

                    self.package_name = scoped_id_node.text

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
                            raise Exception(
                                "unhandled situation in import_declaration!"
                            )

                case "class_declaration":
                    # the node of the identifier
                    id_node = node.named_children[1]
                    if id_node.type != "identifier":
                        raise Exception("unhandled situation in class_declaration!")

                    match node.named_children[0].text.decode():
                        case "public":
                            self.public_class_list.append(id_node.text.decode())
                        case _:
                            raise Exception(
                                "unhandled situation in class_declaration!",
                                node.named_children[0].text,
                            )

                    for child_node in node.named_children:
                        # print(" ", child_node.type, child_node.text.decode())
                        analyze_node(child_node)
                
                # case "class_body":
                #     for child_node in node.named_children:
                #         print(" ", child_node.type, child_node.text.decode())

                    

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
    print(test_java_analyzer.public_class_list)
