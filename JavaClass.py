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
        self.dependency_set: Set[str] = set()  # the of id of the classes it depends on
