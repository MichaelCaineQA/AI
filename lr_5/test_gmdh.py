import unittest
import os

from gmdh import GMDH


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


class Tests(unittest.TestCase):

    def test_gmdh(self):
        n_lines = 0
        m = 0  # Число признаков (Входных элементов). Число 6 в datafile.txt
        N = 0  # Число образцов выборки (N = NA + NB). Число 16 в файле datafile.txt
        NA = 0  # Число 8 в файле datafile.txt
        x = []  # input_data. Числовые значения после имени класса (High/Normal) в файле datafile.txt
        y = []  # 1 если класс High, 0 если класс Normal
        # Чтение значений
        for line in open(os.path.join(PROJECT_ROOT, 'datafile.txt'), 'r').readlines():
            if n_lines == 0:
                N, m, NA = line.rstrip('\n').split(' ')
                m = int(m)
                N = int(N)
                NA = int(NA)
                n_lines += 1
                continue
            items = line.rstrip('\n').split(' ')

            class_name = items[0]
            if class_name == 'High':
                y.append(1)
            elif class_name == 'Normal':
                y.append(0)

            vect = items[1:]
            # make it float
            for i in range(len(vect)):
                vect[i] = float(vect[i])
            x.append(vect)
            n_lines += 1

        gmdh = GMDH(m, N, NA, x, y)
        gmdh.training()
        gmdh.goBack()
        gmdh.printGMDH()
        # print("Normal: ", gmdh.testGMDH([0.279, 0.856, 0.350, 0.870, 3234.801, 114920.842]))
        # print("High: ", gmdh.testGMDH([0.294, 2.828, 0.125, 0.205, 12712.210, 102701.833]))
        # print("High: ", gmdh.testGMDH([2.944, 1.905, 0.650, 0.688, 22068.982, 180123.185]))


        # print ("### TEST ###")
        # for line in open(os.path.join(PROJECT_ROOT, 'datafile_all.txt'), 'r').readlines():
        #     items = line.rstrip('\n').split(' ')
        #     class_name = items[0]
        #     vect = items[1:]
        #     # make it float
        #     for i in range(len(vect)):
        #         vect[i] = float(vect[i])
        #     res = gmdh.testGMDH(vect)
        #     print(class_name, ":", res, " ->", round(res))


if __name__ == '__main__':
    unittest.main()
