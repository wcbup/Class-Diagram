from __future__ import annotations
from typing import List, Tuple
import glob


def load_java_files(project_name: str) -> list[Tuple[str, str]]:
    """
    load all the contents of java files in the project
    return a list of tuples of file name and content
    """
    file_paths: List[str] = []
    # find all java files in the project
    for file_path in glob.glob("./" + project_name + "/**/*.java", recursive=True):
        file_paths.append(file_path)

    # print(file_paths)

    def get_name(path: str) -> str:
        """
        get the name of the java file from the path
        """
        dot_loc = path.rfind(".")
        file_name = path[:dot_loc]
        slash_loc = file_name.rfind("\\")
        file_name = file_name[slash_loc + 1 :]
        return file_name

    # the list containing tuples of name and content
    name_content_list: List[Tuple[str, str]] = []
    for file_path in file_paths:
        with open(file_path, "r") as file:
            name_content_list.append((get_name(file_path), file.read()))
    
    # for name, content in name_content_list:
    #     print(name)
    #     print(content)
    #     print("----------")

    return name_content_list


# test code
if __name__ == "__main__":
    load_java_files("example-dependency-graphs")
