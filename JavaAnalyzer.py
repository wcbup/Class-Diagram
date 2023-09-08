from __future__ import annotations
from typing import List, Set
from load_java_files import load_java_files
import tree_sitter
from JavaClass import JavaClass


class JavaAnalyzer:
    """
    class for analyzing one java file
    """

    def __init__(self, name: str, content: str) -> JavaAnalyzer:
        self.id = ""  # the id of the java file, e.g. dtu.compute.util.Utils
        self.name = name  # the name of the java file
        self.content = content  # the content of the java file
        self.package_name = ""  # the name of package it belongs to
        self.import_file_set: Set[
            str
        ] = set()  # the set of names of the files it imports
        self.import_package_set: Set[
            str
        ] = set()  # the set of names of the packages it imports
        self.public_class_set: Set[
            JavaClass
        ] = set()  # the set of public classes it creates

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

        def analyze_node(
            node: tree_sitter.Node, debug_level: int, current_class: JavaClass | None
        ):
            """
            analyze one node

            :param node: the node currently analyzing
            :param debug_level: help to format the debug output
            :param current_class: the javaclass currently focus on
            """

            def debug_analyze_child() -> None:
                """
                print the types of children of the node
                analyze all the children
                """
                for child_node in node.named_children:
                    print(" " * debug_level, child_node.type)
                    analyze_node(child_node, debug_level + 1, current_class)

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
                    analyze_node(child_node, debug_level + 1, current_class)

            match node.type:
                case "package_declaration":
                    debug_analyze_child()

                    # scoped_identifier
                    scoped_id_node = node.named_children[0]
                    if scoped_id_node.type != "scoped_identifier":
                        raise Exception("unhandled situation in package_declaration")

                    self.package_name = scoped_id_node.text.decode()
                    # set up id
                    self.id = self.package_name + "." + self.name

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
                    # print_child_type_text()

                    # the node of the identifier
                    id_node = node.named_children[1]
                    if id_node.type != "identifier":
                        raise Exception("unhandled situation in class_declaration!")

                    match node.named_children[0].text.decode():
                        case "public":
                            # create new java class
                            new_class = JavaClass(
                                self.package_name, id_node.text.decode()
                            )
                            self.public_class_set.add(new_class)
                            current_class = new_class  # change current focus class
                        case _:
                            raise Exception(
                                "unhandled situation in class_declaration!",
                                node.named_children[0].text,
                            )

                    debug_analyze_child()

                case "modifiers":
                    print_debug_info(node.text)
                    # print_child_type_text()

                case "identifier":
                    print_debug_info(node.text)

                case "class_body":
                    debug_analyze_child()

                case "field_declaration":
                    type_node = node.named_children[0]  # the node for type
                    if type_node.type == "type_identifier":
                        current_class.aggregate_name_set.add(type_node.text.decode())

                    debug_analyze_child()

                case "type_identifier":
                    print_debug_info(node.text)
                    current_class.depend_name_set.add(node.text.decode())

                case "void_type":
                    print_debug_info(node.text)

                case "array_type":
                    debug_analyze_child()

                case "dimensions":
                    print_debug_info(node.text)

                case "variable_declarator":
                    print_debug_info(node.text)

                case "method_declaration":
                    debug_analyze_child()

                case "formal_parameters":
                    debug_analyze_child()

                case "formal_parameter":
                    debug_analyze_child()

                case "block":
                    debug_analyze_child()

                case "expression_statement":
                    debug_analyze_child()

                case "method_invocation":
                    # print_child_type_text()

                    first_child = node.named_children[0]
                    match first_child.type:
                        case "identifier":
                            current_class.depend_name_set.add(first_child.text.decode())
                        case "field_access":
                            pass  # handle it next level
                        case _:
                            raise Exception("unhandled case in method_invocation")

                    debug_analyze_child()

                case "field_access":
                    current_class.depend_field_set.add(node.text.decode())
                    print_debug_info(node.text)
                    # debug_analyze_child()

                case "argument_list":
                    print_debug_info(node.text)

        for node in self.root_node.named_children:
            print(node.type)
            analyze_node(node, 0, None)

        print()
        print("id:", self.id)
        print("import files:", self.import_file_set)
        print("import packages:", self.import_package_set)
        print("public classes:", [i.id for i in self.public_class_set])
        print()

        for java_class in self.public_class_set:
            print(java_class.id)
            print(" ", "aggregate name set:", java_class.aggregate_name_set)
            print(" ", "depend name set:", java_class.depend_name_set)
            print(" ", "depend field set:", java_class.depend_field_set)
            print()

        # add the dependency from java lang
        # add the dependency left in field set
        for java_class in self.public_class_set:
            java_class.add_lang_dependency()
            java_class.add_dependency_in_field()

        for java_class in self.public_class_set:
            print(java_class.id)
            print(" ", "aggregate name set:", java_class.aggregate_name_set)
            print(" ", "depend name set:", java_class.depend_name_set)
            print(" ", "depend field set:", java_class.depend_field_set)
            print(" ", "aggregate id set:", java_class.aggregate_id_set)
            print(" ", "depend id set:", java_class.depend_id_set)
            print()

    def check_dependency(self, java_analyzer: JavaAnalyzer) -> None:
        """
        check if its classes depend on classes from another java_analyzer
        add them if identify dependencies
        """
        # check if it imports java_analyzer
        if (
            self.package_name == java_analyzer.package_name
            or java_analyzer.id in self.import_file_set
            or java_analyzer.package_name in self.import_package_set
        ):
            for source_class in java_analyzer.public_class_set:
                for java_class in self.public_class_set:
                    java_class.add_dependency_if_depend(source_class)


# test code
if __name__ == "__main__":
    # name_content_list = load_java_files("course-02242-examples")
    name_content_list = load_java_files("example-dependency-graphs")
    java_analyzer_list: list[JavaAnalyzer] = []
    for name, content in name_content_list:
        java_analyzer_list.append(JavaAnalyzer(name, content))
        java_analyzer_list[-1].analyze()

    # for java_analyzer in java_analyzer_list:
    #     java_analyzer.analyze()

    for i in java_analyzer_list:
        for j in java_analyzer_list:
            if i == j:
                continue
            else:
                i.check_dependency(j)

    # test_java_analyzer = java_analyzer_list[0]
    # test_java_analyzer.analyze()

    print("---------")
    for java_analyzer in java_analyzer_list:
        for java_class in java_analyzer.public_class_set:
            print(java_class.id)
            print(" ", "aggregate name set:", java_class.aggregate_name_set)
            print(" ", "depend name set:", java_class.depend_name_set)
            print(" ", "depend field set:", java_class.depend_field_set)
            print(" ", "aggregate id set:", java_class.aggregate_id_set)
            print(" ", "depend id set:", java_class.depend_id_set)
            print()
