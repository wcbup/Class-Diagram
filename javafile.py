from __future__ import annotations
import re
import os
from typing import List, Dict


def modify_path(path, num_elements_to_remove, file_extension):
    # Split the path into parts
    parts = path.split(os.path.sep)

    # Remove the specified number of elements from the beginning
    remaining_parts = parts[num_elements_to_remove:]

    # Remove file extension and join parts with dots
    modified_path = ".".join(remaining_parts).replace(file_extension, "").replace(os.path.sep, ".")

    return modified_path
# the class represent a java file
class JavaFile:
    def __init__(self) -> None:
        self.id = ""  # the identification of the java file, e,g. dtu.deps.tricky.Example
        self.file_name = ""  # the name of the java file, e.g. Example
        self.own_class_list: List[str] = []  # the classes owned by the file, e.g. ["Tricky"]
        self.total_str = ""  # the string containing all the text in the file
        self.package_name = "" # the name of the package the file belonging to
        self.import_file_list: List[str] = [] # the files imported by the file, i.e. ['dtu.deps.util.Util']
        self.import_package_list: List[str] = [] # the packages imported by the file, i.e. ['dtu.deps.util']
        self.new_class_list: List[str] = [] # the class newed by the file
        self.dependency_list: List[str] = [] # the dependency list of the java file

    def load_file(self, file_path: str) -> None:
        """
        load text of the java file into 'total_str'
        """
        tmp_file = open(file_path, "r")

        # read all the lines in the file
        str_list = tmp_file.readlines()
        for line in str_list:
            self.total_str += line  # add each line to 'total_str'
        self.file_name = modify_path(file_path,4,".java")
        # print(self.file_name)
        tmp_file.close()
        return self.file_name
    
    def remove_regex(self, reg_pattern: str) -> None:
        """
        remove the strings matching the reg_pattern in 'total_str'
        """
        # replace the matched strings with empty string, i.e. remove all the matching pattern
        self.total_str = re.sub(reg_pattern, "", self.total_str)

    def remove_comment(self) -> None:
        """
        remove the comments in the 'total_str'
        """
        regex_pattern = "\/\/.*|\/\*(.|\n)*?\*\/" # the regular expression for comment
        
        # replace the comments with empty string, i.e. remove all the comments
        self.remove_regex(regex_pattern)

    def remove_string(self) -> None:
        """
        remove the strings in the 'total_str'
        """
        regex_pattern = "\"\"\"\n(.|\n)*?\"\"\"" # the regular expression for string blockhh
        self.remove_regex(regex_pattern) # remove string block
        
        regex_pattern = "\".*?\"" # the regular expression for one-line string
        self.remove_regex(regex_pattern) # remove one-line string
    
    def get_package_name(self) -> None:
        """
        get the package_name from the 'total_str'
        """
        regex_pattern = "package\s+[\w.]+" # the regular expression for package
        match_result: re.Match = re.search(regex_pattern, self.total_str) # search the package name

        if match_result == None:
            raise Exception(f"Can't find package name in {self.file_name}")
        
        # get the name of the package
        match_string: str = match_result.group()
        self.package_name = match_string.split(" ")[-1]
        # print(self.package_name)

    def get_id_and_package(self) -> None:
        """
        get the package_name and id of the java file
        """
        self.get_package_name()
        # get the file name from self.file_name
        dot_location = self.file_name.rfind(".")
        file_name = self.file_name[dot_location + 1:]
        self.id = self.package_name + "." + file_name
        # print(self.id)
    
    def get_own_class_list(self) -> None:
        """
        get the owned class list of the java file
        """
        regex_pattern = "public\s+class\s+[\w.]+" # the regular expression for public class
        match_results: List[re.Match] = re.findall(regex_pattern, self.total_str)
        
        # get the name of the class
        for result in match_results:
            self.own_class_list.append(result.split(" ")[-1])
        # print(self.own_class_list)
    
    def get_import_file_list(self) -> None:
        """
        get imported file list of the java file
        """
        regex_pattern = "import\s+[\w.]+\s*;" # the regular expression for import file
        match_results: List[re.Match] = re.findall(regex_pattern, self.total_str)

        # get the name of the imported file
        for result in match_results:
            tmp_str_list: List[str] = result.split(" ")
            for tmp_str in tmp_str_list[1:]:
                if len(tmp_str) > 1:
                    # remove ';'
                    semicolon_loc = tmp_str.rfind(";")
                    if semicolon_loc != -1:
                        tmp_str = tmp_str[:semicolon_loc]
                    self.import_file_list.append(tmp_str)
                    break

        # print(self.id, self.import_file_list)

        # add imported file to dependency list
        for file in self.import_file_list:
            self.dependency_list.append(file)

    def get_import_package_list(self) -> None:
        """
        get imported package list of the java file
        """
        regex_pattern = "import\s+[\w.]+\*\s*;" # the regular expression for import package
        match_results: List[re.Match] = re.findall(regex_pattern, self.total_str)

        # get the name of the imported packages
        for result in match_results:
            tmp_str_list: List[str] = result.split(" ")
            for tmp_str in tmp_str_list[1:]:
                if len(tmp_str) > 1:
                    # remove '.*'
                    dot_location = tmp_str.rfind(".")
                    self.import_package_list.append(tmp_str[:dot_location])
                    break
        # print(self.id, self.import_package_list)
    
    def get_new_class_list(self) -> None:
        """
        get the list of the class newed by the file
        """
        regex_pattern = "new\s+\w+" # the regular expression for new class
        match_results: List[re.Match] = re.findall(regex_pattern, self.total_str)

        # get the names of the newed classes
        for result in match_results:
            self.new_class_list.append(result.split(" ")[-1])

        # remove duplicates
        self.new_class_list = list(set(self.new_class_list))
    
    def init(self) -> None:
        """
        initialize the JavaFile,
        remove all the comments and strings,
        get the package name and id,
        get owned class list,
        get imported class list,
        get imported package list
        get newed class list
        add dependencies from lang
        """
        self.remove_comment()
        self.remove_string()
        self.get_id_and_package()
        self.get_own_class_list()
        self.get_import_file_list()
        self.get_import_package_list()
        self.get_new_class_list()
        self.add_lang_dependency()

        # print(self.id, self.own_class_list, self.import_file_list, self.import_package_list, self.new_class_list)
    
    def add_dependency_if_depended(self, java_file: JavaFile) -> None:
        """
        add the id of 'java_file' to the dependency list if it depends on 'java_file'
        """
        # return if it's already recored
        if java_file.id in self.dependency_list:
            return

        # check if package list matched
        if java_file.package_name in self.import_package_list or java_file.package_name == self.package_name:
            # print(java_file.id, "is found in", self.id)
            for owned_class in java_file.own_class_list:
                # check if its class is used
                if owned_class in self.new_class_list:
                    # print("found", owned_class, "from", java_file.id, "in", self.id)
                    self.dependency_list.append(java_file.id)
                    return
        
        # check direct import
        result = re.search(java_file.id, self.total_str)
        if result != None:
            self.dependency_list.append(java_file.id)

    def add_lang_dependency(self) -> None:
        """
        add the dependencies from lang
        """
        lang_dependencies_list = [
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
        ]
        
        # check if the classes in lang are used
        for class_name in lang_dependencies_list:
            result = re.search(class_name, self.total_str)
            if result != None:
                self.dependency_list.append("java.lang." + class_name)

# class that draws the dependency graph
class Painter:
    def __init__(self) -> None:
        self.javafile_list: List[JavaFile] = [] # the list containing all the javafile
        self.dot_code = "" # the dot code representing the graph
    
    def add_one(self, java_file: JavaFile) -> None:
        """
        add one java file to the list
        """
        self.javafile_list.append(java_file)
    
    def generate_dot_code(self) -> None:
        """
        generate the dot code
        save the code into './result.dot'
        """
        dot_id_map: Dict[str, str] = {} # the map for javafile id and dot id
        self.dot_code = "digraph SourceGra {\n" # the code for the dot file
        dot_id = 0 # the id for javafile in dot code

        # allocate the dot id to each javafile
        for java_file in self.javafile_list:
            if java_file.id not in dot_id_map:
                dot_id_map[java_file.id] = str(dot_id)
                dot_id += 1

            for tmp_file_id in java_file.dependency_list:
                if tmp_file_id not in dot_id_map:
                    dot_id_map[tmp_file_id] = str(dot_id)
                    dot_id += 1
        
        for java_id in dot_id_map:
            self.dot_code += f"x{dot_id_map[java_id]} [label = \"{java_id}\";\n]"

        for java_file in self.javafile_list:
            for depend_file_id in java_file.dependency_list:
                self.dot_code += f"x{dot_id_map[java_file.id]} -> x{dot_id_map[depend_file_id]};\n"
        
        self.dot_code += "}" # add last brace

        dot_file_path = "./result.dot"
        with open(dot_file_path, "w") as f:
            f.write(self.dot_code)

    def generate_graph_and_show(self) -> None:
        """
        generate the graph using dot
        """
        self.generate_dot_code()
        command = f".\\Graphviz\\bin\\dot.exe -Tpng .\\result.dot -o result.png"
        os.system(command)
        command = f".\\result.png"
        os.system(command)
        # print(command)

# test code
if __name__ == "__main__":
    import glob

    root_directory_path = "example-dependency-graphs"
    file_paths = []
    # find all the files ending with '.java'
    for file_path in glob.glob("./" + root_directory_path + "/**/*.java", recursive=True):
        file_paths.append(file_path)
    
    java_file_list: List[JavaFile] = []

    for file_path in file_paths:
        tmp_java_file = JavaFile()
        filename = tmp_java_file.load_file(file_path)
        # tmp_java_file.remove_comment()
        # tmp_java_file.remove_string()
        # # tmp_java_file.get_package_name()
        # tmp_java_file.get_id_and_package()
        # tmp_java_file.get_own_class_list()
        # tmp_java_file.get_import_file_list()
        # tmp_java_file.get_import_package_list()
        tmp_java_file.init()
        java_file_list.append(tmp_java_file)

        # print(root_directory_path, file_path)
        # print(tmp_java_file.total_str) # print the text in the file
        with open(filename + ".txt", "w") as f:
            f.write(tmp_java_file.total_str)
    
    # add dependency
    for java_file in java_file_list:
        for tmp_java_file in java_file_list:
            if java_file == tmp_java_file:
                continue
            java_file.add_dependency_if_depended(tmp_java_file)
    
    # show the dependencies
    for java_file in java_file_list:
        print(java_file.id, java_file.dependency_list)

    painter = Painter()

    for java_file in java_file_list:
        painter.add_one(java_file)
    
    painter.generate_dot_code()
    # print(painter.dot_code)
    painter.generate_graph_and_show()

