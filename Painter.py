from __future__ import annotations
from JavaClass import JavaClass
from typing import List, Dict, Set
import os


class Painter:
    """
    class that draws the dependency graph
    """

    def __init__(self) -> None:
        self.java_class_set: Set[JavaClass] = set()
        self.dot_code = ""  # the dot code representing the graph

    def add_one(self, java_class: JavaClass) -> None:
        """
        add one java class to the list
        """
        self.java_class_set.add(java_class)

    def generate_dot_code(self) -> None:
        """
        generate the dot code
        save the code into './result.dot'
        """
        dot_id_map: Dict[str, str] = {}  # java class id maps to dot id
        self.dot_code = "digraph SourceGra {\n"
        self.dot_id = 0  # the id for java class in dot class

        def allocate_id(java_class_id: str) -> None:
            """
            allocate the id to java class if it doesn't have one
            """
            if java_class_id in dot_id_map:
                return
            else:
                dot_id_map[java_class_id] = str(self.dot_id)
                self.dot_id += 1

        # allocate the dot id to java class
        for java_class in self.java_class_set:
            allocate_id(java_class.id)

            for tmp_file_id in java_class.aggregate_id_set:
                allocate_id(tmp_file_id)
            for tmp_file_id in java_class.depend_id_set:
                allocate_id(tmp_file_id)

        for java_class_id in dot_id_map:
            self.dot_code += (
                f'x{dot_id_map[java_class_id]} [label = "{java_class_id}"];\n'
            )

        for java_class in self.java_class_set:
            for aggregate_class_id in java_class.aggregate_id_set:
                self.dot_code += f'x{dot_id_map[java_class.id]} -> x{dot_id_map[aggregate_class_id]} [label = "aggregation"];\n'
            for depend_class_id in java_class.depend_id_set:
                if depend_class_id not in java_class.aggregate_id_set:
                    self.dot_code += f'x{dot_id_map[java_class.id]} -> x{dot_id_map[depend_class_id]} [label = "dependency"];\n'
        
        self.dot_code += "}"

        dot_file_path = "./result.dot"
        with open(dot_file_path, "w") as f:
            f.write(self.dot_code)
        
    def generate_graph_and_show(self) -> None:
        """
        generate the graph
        save the graph to './result.png'
        show the graph
        """

        DPI = 500 # the dpi of the result picture
        self.generate_dot_code()
        command = f".\\Graphviz\\bin\\dot.exe -Tpng -Gdpi={DPI} .\\result.dot -o result.png"
        os.system(command)
        command = ".\\result.png"
        os.system(command)
