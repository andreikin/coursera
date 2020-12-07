import os
import tempfile


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
        sumfile_path = os.path.join(tempfile.gettempdir(), 'storage.data')
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



# fl = File('test.txt')
# print(fl.is_path_exists())
#
# fl.write('gggggggg')
#
# print(fl.read())


path_to_file = 'some_filename'
print(os.path.exists(path_to_file))
#False
file_obj = File(path_to_file)
print(os.path.exists(path_to_file))
# #True
#print(file_obj.read())
# #''
#file_obj.write('some text')

print(file_obj.read())
# 'some text'
file_obj.write('other text')

file_obj.read()
# #'other text'
# file_obj_1 = File(path_to_file + '_1')
# file_obj_2 = File(path_to_file + '_2')
# file_obj_1.write('line 1\n')
# #7
# file_obj_2.write('line 2\n')
# #7
# new_file_obj = file_obj_1 + file_obj_2
# isinstance(new_file_obj, File)
# #True
# print(new_file_obj)
# #C:\Users\Media\AppData\Local\Temp\71b9e7b695f64d85a7488f07f2bc051c
# for line in new_file_obj:
#     print(ascii(line))
# #'line 1\n'
# #'line 2\n'