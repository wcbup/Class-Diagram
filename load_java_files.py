from __future__ import annotations
from typing import List
import glob


def load_java_files(project_name: str) -> list[str]:
    """
    load all the contents of java files in the project
    """
    file_paths: List[str] = []
    for file_path in glob.glob("./" + project_name + "/**/*.java", recursive=True):
        file_paths.append(file_path)

    # print(file_paths)

    content_list: List[str] = []
    for file_path in file_paths:
        with open(file_path, "r") as file:
            content_list.append(file.read())

    return content_list


# test code
if __name__ == "__main__":
    load_java_files("example-dependency-graphs")
