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
        self.inherit_set: Set[str] = set()  # the of id of the classes it extends
        self.realize_set: Set[str] = set()  # the of id of the classes it implement
        self.aggregate_set: Set[
            str
        ] = set()  # the of id of the classes its field contains
        self.compose_set: Set[
            str
        ] = set()  # the of id of the classes its nonstatic innerclass
        self.depend_set: Set[str] = set()  # the of id of the classes it depends on

    def __hash__(self) -> int:
        return self.id.__hash__()

    def __eq__(self, __value: JavaClass) -> bool:
        return self.id == __value.id

    def __str__(self) -> str:
        return self.id