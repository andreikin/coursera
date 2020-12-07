import os


class File:
    """При создании экземпляра класса File в конструктор передается полный путь
     до файла на файловой системе. Если файла с таким путем не существует,
     он должен быть создан при инициализации."""
    def __init__(self, path):
        self.path = path
        if not self.is_path_exists():
            self.write('')

    """- сложение объектов типа File, результатом сложения является объект класса File, 
    при этом создается новый файл и файловый объект, в котором содержимое второго файла 
    добавляется к содержимому первого файла. Новый файл должен создаваться в директории, 
    полученной с помощью функции tempfile.gettempdir. Для получения нового пути можно 
    использовать os.path.join."""
    def __add__(self, other):
        pass

    """- возвращать в качестве строкового представления объекта класса File полный путь до файла"""
    def __str__(self):
        return 'Class File ' + self.path

    """- поддерживать протокол итерации, причем итерация проходит по строкам файла"""
    def __getitem__(self, item):
        pass

    """- чтение из файла, метод read возвращает строку с текущим содержанием файла"""
    def read(self):
        try:
            with open(self.path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return ""

    """- запись в файл, метод write принимает в качестве аргумента строку с новым содержанием файла"""
    def write(self, line):
        with open(self.path, 'w') as file:
            return file.write(line)

    def is_path_exists(self):
        return os.path.exists(self.path)



fl = File('test.txt')
print(fl.is_path_exists())

#fl.write('gggggggg')

print(fl.read())
