from __future__ import annotations
from typing import Set


class JavaClass:
    """
    the class representing a java class
    """

    def __init__(self, package_name: str, class_name: str) -> None:
        self.id = package_name + "." + class_name
        self.package_name = package_name
        self.name = class_name

        """
        name sets serve as 'temporary' set
        once we can identify their specific source, we move them into id set
        """
        self.inherit_id_set: Set[str] = set()  # the id of the classes it extends
        self.inherit_name_set: Set[str] = set()  # the name of the classes it extends

        self.realize_id_set: Set[str] = set()  # the id of the classes it implement
        self.realize_name_set: Set[str] = set()  # the name of the classes it implement

        self.aggregate_id_set: Set[
            str
        ] = set()  # the id of the classes its field contains
        self.aggregate_name_set: Set[
            str
        ] = set()  # the name of the classes its field contains

        self.compose_id_set: Set[
            str
        ] = set()  # the id of the classes its nonstatic innerclass
        self.compose_name_set: Set[
            str
        ] = set()  # the name of the classes its nonstatic innerclass

        self.depend_id_set: Set[str] = set()  # the id of the classes it depends on
        self.depend_name_set: Set[str] = set()  # the id of the classes it depends on

        self.depend_field_set: Set[str] = set()  # the fields it depends on

    def add_lang_dependency(self) -> None:
        """
        add the dependencie from lang
        """
        lang_dependencies_set: Set[str] = {
            "Boolean",
            "Byte",
            "Character",
            "Class",
            "ClassLoader",
            "ClassValue",
            "Compiler",
            "Double",
            "Enu",
            "Float",
            "InheritableThreadLoca",
            "Integer",
            "Long",
            "Math",
            "Number",
            "Object",
            "Package",
            "Process",
            "ProcessBuilder",
            "Runtime",
            "RuntimePermission",
            "SecurityManager",
            "Short",
            "StackTraceElement",
            "StrictMath",
            "String",
            "StringBuffer",
            "StringBuilder",
            "System",
            "Thread",
            "ThreadGroup",
            "ThreadLocal",
            "Throwable",
            "Void",
        }

        def add_lang_prefix(name: str) -> str:
            return "java.lang." + name

        for name in list(self.aggregate_name_set):
            if name in lang_dependencies_set:
                self.aggregate_id_set.add(add_lang_prefix(name))
                self.aggregate_name_set.remove(name)

        for name in list(self.depend_name_set):
            if name in lang_dependencies_set:
                self.depend_id_set.add(add_lang_prefix(name))
                self.depend_name_set.remove(name)

        for field_name in list(self.depend_field_set):
            # get the first identifier of the field
            dot_loc = field_name.find(".")
            name = field_name[:dot_loc]
            if name in lang_dependencies_set:
                self.depend_id_set.add(add_lang_prefix(name))
                self.depend_field_set.remove(field_name)

    def __hash__(self) -> int:
        return self.id.__hash__()

    def __eq__(self, __value: JavaClass) -> bool:
        return self.id == __value.id

    def __str__(self) -> str:
        return self.id
