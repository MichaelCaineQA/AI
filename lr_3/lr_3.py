#!/usr/bin/python
# -*- coding: cp1251 -*-

import math
import random
import sys

from hopfield.parser import parse, parse_shape, SHAPE_SIDE

dictionary = {-1: '-', 1: '@'}


def cmp(a, b):
    if a < b:
        return -1
    if a == b:
        return 0
    if a > b:
        return 1


def charfor(x):
    return dictionary[x]


def printshape(obraz, size):
    i = 0
    out_str = ""
    for o in obraz:
        out_str += str(charfor(o))
        i += 1
        if i % size == 0:
            print(out_str)
            out_str = ""


# ��������� ���� ��������
class HopfieldNet:

    # ������������� ����
    def __init__(self, shapeside):
        self.drawsteps = False
        self.W = []  # ������� ������� �������������
        self.shapes = []  # ������, ������� ������� ����
        self.neurons = int(math.pow(shapeside, 2))  # ���������� ��������
        self.shapeside = shapeside  # ���������� ��� � ������� ������
        r = range(0, self.neurons)
        for i in r:
            self.W.append([0 for x in r])
        self.maxjunkiters = 200  # ������������ ����� ��������������� ��������
        self.junkiter = 0  # ������� ��������������� ��������

    # �������� ���� ������
    def teach(self, shape):
        self.shapes.append(shape)
        self.X = shape
        r = range(0, self.neurons)
        for i in r:
            for j in r:
                if i == j:
                    self.W[i][j] = 0
                else:
                    self.W[i][j] += self.X[i] * self.X[j]

    #
    # ���������� ��������� �����
    #
    def recognize(self, shape):
        self.Y = shape
        iter = 0
        # ���� �� ������� � ����� �� ���������...
        while self.shapes.count(self.Y) == 0:
            self.recstep()
            iter += 1
            # ... ��� ���������� ��������������� �������� �� �������
            if self.junkiter >= self.maxjunkiters:
                return False, self.Y, iter
        return True, self.Y, iter

    # ��� �������������.
    # �������� ���������� ������ ��� ����������
    def recstep(self):
        signum = lambda x: cmp(x, 0)

        r = random.randrange(0, self.neurons, 1)
        net = 0
        for i in range(0, self.neurons):
            net += self.Y[i] * self.W[i][r]
        signet = signum(net)
        if signet != self.Y[r]:  # �������� ������� ������
            print(f"Neuron {r} : {self.Y[r]}  ->  {signet}")
            self.Y[r] = signet
            if self.drawsteps:
                printshape(self.Y, self.shapeside)

            self.junkiter = 0
        else:
            self.junkiter += 1


knows_shapes_dir = "known_shapes"
modified_shape_path = "modified_shapes/modified.txt"


# ������� �������
def main(argv):
    shapes = parse(knows_shapes_dir)
    shape = parse_shape(modified_shape_path)

    print("Known Shapes:")
    for o in shapes:
        printshape(o, SHAPE_SIDE)
        print(o)

    print("Teaching...")
    hopfield = HopfieldNet(SHAPE_SIDE)
    for shp in shapes:
        hopfield.teach(shp)

    print("Modified shape:")
    printshape(shape, SHAPE_SIDE)

    print("Shape recognizing...")
    (recognized, recshape, iters) = hopfield.recognize(shape)

    if recognized:
        print("Success. Shape recognized in %g iterations:" % iters)
    else:
        print("Fail. Shape not recognized in %g iterations..." % iters)
    printshape(recshape, SHAPE_SIDE)


# ����� �����
if __name__ == '__main__':
    main(sys.argv[1:])
