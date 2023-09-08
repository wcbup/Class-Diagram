from __future__ import annotations
from typing import List, Set
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
        self.import_file_set: Set[
            str
        ] = set()  # the set of names of the files it imports
        self.import_package_set: Set[
            str
        ] = set()  # the set of names of the packages it imports
        self.public_class_set: Set[str] = set()  # the set of public classes it creates
        self.use_class_set: Set[str] = set()  # the set of the classes it uses

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

        def analyze_node(node: tree_sitter.Node, debug_level: int):
            """
            analyze one node
            """

            def debug_analyze_child() -> None:
                """
                print the types of children of the node
                analyze all the children
                """
                for child_node in node.named_children:
                    print(" " * debug_level, child_node.type)
                    analyze_node(child_node, debug_level + 1)
            
            def print_child_type_text() -> None:
                """
                print the types and texts of children of the node
                """
                for child_node in node.named_children:
                    print(" " * debug_level, child_node.type, child_node.text)
            
            def print_debug_info(info: str | bytes) -> None:
                """
                print the debug info
                """
                print(" " * debug_level, info)
            
            def analyze_child_node() -> None:
                """
                analyze all the children nodes
                """
                for child_node in node.named_children:
                    analyze_node(child_node, debug_level + 1)

            match node.type:
                case "package_declaration":
                    debug_analyze_child()

                    # scoped_identifier
                    scoped_id_node = node.named_children[0]
                    if scoped_id_node.type != "scoped_identifier":
                        raise Exception("unhandled situation in package_declaration")

                    self.package_name = scoped_id_node.text

                case "import_declaration":
                    debug_analyze_child()

                    # scoped_identifier
                    scoped_id_node = node.named_children[0]
                    if scoped_id_node.type != "scoped_identifier":
                        raise Exception("import_declaration")

                    match node.named_child_count:
                        case 1:
                            self.import_file_set.add(scoped_id_node.text.decode())
                        case 2:
                            self.import_package_set.add(scoped_id_node.text.decode())
                        case _:
                            raise Exception(
                                "unhandled situation in import_declaration!"
                            )

                case "scoped_identifier":
                    print_debug_info(node.text)
                
                case "asterisk":
                    print_debug_info(node.text)
                
                case "line_comment":
                    # print_debug_info(node.text)
                    return
                
                case "block_comment":
                    # print_debug_info(node.text)
                    return

                case "class_declaration":
                    # the node of the identifier
                    id_node = node.named_children[1]
                    if id_node.type != "identifier":
                        raise Exception("unhandled situation in class_declaration!")

                    match node.named_children[0].text.decode():
                        case "public":
                            self.public_class_set.add(id_node.text.decode())
                        case _:
                            raise Exception(
                                "unhandled situation in class_declaration!",
                                node.named_children[0].text,
                            )

                    debug_analyze_child()
                
                case "modifiers":
                    print_debug_info(node.text)
                
                case "identifier":
                    print_debug_info(node.text)

                case "class_body":
                    debug_analyze_child()

                case "field_declaration":
                    debug_analyze_child()
                    
                case "type_identifier":
                    print_debug_info(node.text)
                    self.use_class_set.add(node.text.decode())

                case "variable_declarator":
                    print_debug_info(node.text)

                case "method_declaration":
                    debug_analyze_child()

                case "formal_parameters":
                    debug_analyze_child()
                
                case "formal_parameter":
                    debug_analyze_child()


        for node in self.root_node.named_children:
            print(node.type)
            analyze_node(node, 0)


# test code
if __name__ == "__main__":
    # name_content_list = load_java_files("course-02242-examples")
    name_content_list = load_java_files("example-dependency-graphs")
    java_analyzer_list: list[JavaAnalyzer] = []
    for name, content in name_content_list:
        java_analyzer_list.append(JavaAnalyzer(name, content))

    test_java_analyzer = java_analyzer_list[0]
    test_java_analyzer.analyze()
    print(test_java_analyzer.import_file_set)
    print(test_java_analyzer.import_package_set)
    print(test_java_analyzer.public_class_set)
    print(test_java_analyzer.use_class_set)
