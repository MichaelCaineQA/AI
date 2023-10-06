from __future__ import with_statement
import os
import string
from os.path import isdir, isfile

MAX_SIZE = 512
SHAPE_SIDE = 7
dictionary = {'-': -1, '@': 1}


#
# —читывает фигуры из файлов и возвращает
# список из их элементов
#
def parse(dir):
    shapes_files = []
    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        if isfile(path):
            shapes_files.append(path)

    shapes = []
    for path in shapes_files:
        shape = parse_shape(path)
        shapes.append(shape)
    return shapes


#
# —читывает файл с фигурой и преобразует
# в список
#
def parse_shape(path):
    with open(path) as f:
        contents = f.read(MAX_SIZE)
        contents = contents.replace("\n", "")
        contents = contents.replace("\r", "")

        shape = []
        for c in contents:
            shape.append(dictionary[c])
        if len(shape) != pow(SHAPE_SIDE, 2):
            raise Exception("Shape size must be %gx%g" % (SHAPE_SIDE, SHAPE_SIDE))
        return shape
