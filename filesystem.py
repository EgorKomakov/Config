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
        if directory.startswith('..'):
            while directory.startswith('../'):
                directory = directory[3:]
                if self.current_directory != '/':
                    self.current_directory = '/'.join(self.current_directory.split('/')[:-2]) + '/'
            if directory:
                self.current_directory = '/'.join(self.current_directory.split('/')[:-2]) + '/'
        elif directory.count('.') != 0:
            self.text_area.insert(tk.END, "Нет такого каталога\n")
        elif directory.startswith('/'):
            if directory in self.zip_path or directory[1:] in self.zip_path:
                self.current_directory = self.current_directory + directory
        elif self.current_directory + directory + '/' in  self.zip_path or self.current_directory[1:] + directory + '/' in self.zip_path:
            self.current_directory = self.current_directory + directory + '/'
        elif self.current_directory + directory in self.zip_path or self.current_directory[1:] + directory in self.zip_path:
            self.current_directory = self.current_directory + directory
        else:
            print("Нет такого каталога")

    def get_current_directory(self):
        return self.current_directory

