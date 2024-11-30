import zipfile
import os

class VirtualFileSystem:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.current_directory = '/'

    def list_files(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_file:
            return [f for f in zip_file.namelist() if f.startswith(self.current_directory)]

    def change_directory(self, directory):
        new_directory = os.path.join(self.current_directory, directory)
        if new_directory in self.list_files():
            self.current_directory = new_directory
            return True
        return False

    def get_current_directory(self):
        return self.current_directory

