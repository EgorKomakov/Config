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