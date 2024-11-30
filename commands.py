import calendar

def ls(filesystem):
    return filesystem.list_files()

def cd(filesystem, directory):
    return filesystem.change_directory(directory)

def exit_shell():
    print("Exiting shell...")
    exit(0)

def cal():
    return calendar.TextCalendar().formatmonth(2024, 11)