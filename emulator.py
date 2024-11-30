"""import os
import zipfile
import yaml
import sys


class VirtualFileSystem:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.current_path = ""

    def list_files(self):
        with zipfile.ZipFile(self.zip_path) as z:
            return [f for f in z.namelist() if f.startswith(self.current_path) or not self.current_path]

    def change_directory(self, new_dir):
        if new_dir in self.list_files():
            self.current_path = new_dir
        else:
            print(f"Путь {new_dir} не найден.")

    def get_current_path(self):
        return self.current_path if self.current_path else "/"


def load_config(config_path):
    with open(config_path) as f:
        return yaml.safe_load(f)


def main():
    config = load_config('config.yaml')
    vfs = VirtualFileSystem(config['vfs_path'])

    while True:
        command = input(f"{vfs.get_current_path()}$ ").strip().split()

        if not command:
            continue
        cmd = command[0]

        if cmd == "ls":
            print("\n".join(vfs.list_files()))
        elif cmd == "cd":
            if len(command) > 1:
                vfs.change_directory(command[1])
            else:
                print("Укажите путь для cd.")
        elif cmd == "exit":
            break
        elif cmd == "cal":
            os.system('cal')
        elif cmd == "rev":
            if len(command) > 1:
                print(command[1][::-1])
            else:
                print("Укажите строку для реверса.")
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()"""
"""import os
import zipfile
import yaml
import calendar


class VirtualFileSystem:
    def __init__(self, zip_path):
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"Error: The file {zip_path} does not exist.")

        self.zip_path = zip_path
        self.current_path = '/'
        self.zip_file = zipfile.ZipFile(zip_path)

    def list_files(self):
        return [name for name in self.zip_file.namelist() if name.startswith(self.current_path)]

    def change_directory(self, path):
        if path == "..":
            self.current_path = '/'.join(self.current_path.split('/')[:-2]) + '/'
        elif path in self.list_files():
            self.current_path = path if path.endswith('/') else path + '/'
        else:
            print(f"cd: no such file or directory: {path}")

    def get_current_directory(self):
        return self.current_path

    def display_calendar(self):
        year = calendar.datetime.datetime.now().year
        month = calendar.datetime.datetime.now().month
        return calendar.month(year, month)

    def reverse_string(self, input_string):
        return input_string[::-1]


def main():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    zip_path = config.get('/Users/egorkomakov/PycharmProjects/DZ1/.venv/lib/python3.9/vfs.zip')

    try:
        vfs = VirtualFileSystem(zip_path)
        while True:
            command = input(f"{vfs.get_current_directory()}$ ")
            if command.startswith("ls"):
                print(vfs.list_files())
            elif command.startswith("cd "):
                path = command[3:].strip()
                vfs.change_directory(path)
            elif command == "cal":
                print(vfs.display_calendar())
            elif command.startswith("rev "):
                input_str = command[4:].strip()
                print(vfs.reverse_string(input_str))
            elif command == "exit":
                break
            else:
                print("Unknown command.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()"""
import yaml
from filesystem import VirtualFileSystem
from commands import ls, cd, exit_shell, cal


def main():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    vfs = VirtualFileSystem(config['filesystem_zip'])

    while True:
        command = input(f"{vfs.get_current_directory()} $ ").strip().split()

        if not command:
            continue

        cmd = command[0]

        if cmd == 'ls':
            files = ls(vfs)
            print('\n'.join(files))
        elif cmd == 'cd':
            if len(command) < 2 or not cd(vfs, command[1]):
                print(f"cd: no such file or directory: {command[1]}")
        elif cmd == 'exit':
            exit_shell()
        elif cmd == 'cal':
            print(cal())
        elif cmd == 'rev':
            if len(command) != 2:
                print("rev: missing argument")
            else:
                print(command[1][::-1])
        else:
            print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()