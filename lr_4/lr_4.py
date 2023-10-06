#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import with_statement

import numpy as np
import os
from os.path import isfile

MAX_SIZE = 512
SHAPE_SIDE = 7
dictionary = {'-': -1, '@': 1}
back_ictionary = {-1: '-', 1: '@'}
SHAPES_PATH = "known_shapes"
INPUT_PATH = "modified_shapes"


def charfor(x):
    return dictionary[x]


def printshape(obraz, size):
    i = 0
    out_str = ""
    for o in obraz:
        out_str += str(back_ictionary[o])
        i += 1
        if i % size == 0:
            print(out_str)
            out_str = ""


#
# ��������� ������ �� ������ � ����������
# ������ �� �� ���������
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
# ��������� ���� � ������� � �����������
# � ������
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


class PotentialMethod:
    def __init__(self):
        self.shapes = parse(SHAPES_PATH)
        self.input = parse(INPUT_PATH)[0]
        self.Ps = [0.0] * len(self.shapes)

    def get_result(self):
        print("Input:")
        printshape(self.input, SHAPE_SIDE)

        # ����� ���������� ���������
        max_p = -1
        idx_max_p = -1
        for i, p in enumerate(self.Ps):
            if p > max_p:
                max_p = p
                idx_max_p = i

        return self.shapes[idx_max_p]

    def potential(self):
        for i, shape in enumerate(self.shapes):
            r = self.compare(self.input, shape)
            self.Ps[i] += 1_000_000 / (1 + r ** 2)

        print("Potentials:")
        print(self.Ps)

    def compare(self, b1, b2):
        count = 0
        assert len(b1) == len(b2)  # ������� ������������ ����� �����
        b1_pixels = self.to_pixels(b1)
        b2_pixels = self.to_pixels(b2)

        for i in range(7):
            for j in range(7):
                if b1_pixels[i][j] != b2_pixels[i][j]:
                    count += 1

        return count

    def to_pixels(self, shape):
        n = int(np.sqrt(len(shape)))
        result = np.zeros((n, n), dtype=int)
        k = 0
        for i in range(n):
            line_int = shape[k:k + n]
            result[i] = line_int
            k += n

        return result


if __name__ == "__main__":
    potential_method = PotentialMethod()
    potential_method.potential()
    result = potential_method.get_result()
    print("Result:")
    printshape(result, SHAPE_SIDE)
