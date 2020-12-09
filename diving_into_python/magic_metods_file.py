import os
import tempfile
import uuid


class File:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            open(self.path, 'w').close()

    def __add__(self, other):
        # generate new path in temp directory and random file name
        sumfile_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4().hex))
        obj = File(sumfile_path)
        obj.write(self.read() + other.read())
        return obj

    def __str__(self):
        return self.path

    def __getitem__(self, item):
        with open(self.path, 'r') as file:
            text = file.readlines()
        return text[item]

    def read(self):
        with open(self.path, 'r') as file:
            return file.read()

    def write(self, line):
        with open(self.path, 'w') as file:
            return file.write(line)
