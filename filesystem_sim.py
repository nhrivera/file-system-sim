# Base class for any file system node (directory and files)
class Node:
    def __init__(self, name, parent=None):
        self.name = name # The name of the node (directory or file)
        self.parent = parent # The parent directory of the node
        self.nextSibling = None # The next sibling node in the directory

# Directory class, inherited from Node and represents a Directory for the file system
class Directory(Node):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.firstChild = None

    # MEthod to add a child node to the directory
    def add_child(self, node):
        if not self.firstChild:
            self.firstChild = node
        else:
            current = self.firstChild
            while current.nextSibling:
                current = current.nextSibling
            current.nextSibling = node

    # Method to find a child node by name
    def find(self, name):
        current = self.firstChild
        while current:
            if current.name == name:
                return current
            current = current.nextSibling
        return None
    
    # Method to print the names of all child nodes in the directory
    def print_contents(self):
        current = self.firstChild
        while current:
            print(current.name, end=' ')
            current = current.nextSibling
        print()

# File class inherits from Node and represents a file for the file system
class File(Node):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)

# FileSystem class manages the file system
class FileSystem:
    def __init__(self):
        self.root = Directory("/")
        self.current_dir = self.root

    # Method to list the contents of the current directory
    def ls(self):
        self.current_dir.print_contents()

    # Method to create a new directory at the current path
    def mkdir(self, path):
        dirs = path.strip("/").split("/")
        current_dir = self.current_dir
        for dir_name in dirs:
            found = current_dir.find(dir_name)
            if not found:
                new_dir = Directory(dir_name, current_dir)
                current_dir.add_child(new_dir)
                current_dir = new_dir
            elif isinstance(found, Directory):
                current_dir = found
            else:
                print("A file with the same name already exists. ")

    # Method to change the current directory        
    def cd(self, path):
        if path == "/":
            self.current_dir = self.root
            return
        elif path == "..":
            if self.current_dir.parent is not None:
                self.current_dir = self.current_dir.parent
            return
        else:
            dirs = path.strip("/").split("/")
            current_dir = self.current_dir
            for dir_name in dirs:
                if dir_name == "..":
                    if current_dir.parent is not None:
                        current_dir = current_dir.parent
                else:
                    found = current_dir.find(dir_name)
                    if found and isinstance(found, Directory):
                        current_dir = found
                    else:
                        print("Directory not found: " + path)
                        return
            self.current_dir = current_dir
    
    # Method used to create a new file to the current directory
    def touch(self, name):
        new_file = File(name, self.current_dir)
        self.current_dir.add_child(new_file)

# Main function for the command line interface
def main():
    fs = FileSystem()
    print("File System Simulator. Type 'help' for commands.")

    while True:
        command = input(">").strip().split()
        if not command:
            continue
        if command[0] == "ls":
            fs.ls()
        elif command[0] == "mkdir" and len(command) > 1:
            fs.mkdir(command[1])
        elif command[0] == "cd" and len(command) > 1:
            fs.cd(command[1])
        elif command[0] == "touch" and len(command) > 1:
            fs.touch(command[1])
        elif command[0] == "exit":
            break
        elif command[0] == "help":
            print("Commands:")
            print("   ls - List contents of the current directory")
            print("   mkdir <dir> - Create a new directory")
            print("   cd <dir> - Change directory")
            print("   touch <file> - Create a new file")
            print("   exit - Exit the simulator ")
        else:
            print("Unknown command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()