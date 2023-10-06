import numpy as np


def main():
    arr = np.array([2, 4, 10, 12, 3, 20, 30, 11, 25])
    print("Input: " + str(arr))
    m1, m2 = 0, 0  # Значение центроидов
    m = 0  # Число итераций
    flag = False  # Флаг, который даст знать, что центры масс m1, m2 не меняются
    a, b = arr[0], arr[1]  # a, b сохраняют предыдущее состояние центра масс, чтобы сравнить с текущим значением
    m1, m2 = a, b
    cluster1, cluster2 = [], []

    while not flag:
        sum1, sum2 = 0, 0
        cluster1, cluster2 = [], []
        m += 1  # Подсчет числа итераций
        k, j = 0, 0  # Элементы, которые будут записывать значения в первый и второй массив

        for i in range(len(arr)):
            if abs(arr[i] - m1) <= abs(arr[i] - m2):  # Принимаем за первую центроиду первое значение массива, за вторую - второе и сравниваем
                cluster1.append(arr[i])  # Если проходит, то записываем в первый кластер
                k += 1
            else:
                cluster2.append(arr[i])
                j += 1

        for i in range(k):  # Вычисляем сумму для 1-го кластера
            sum1 += cluster1[i]

        for i in range(j):  # Вычисляем сумму для 2-го кластера
            sum2 += cluster2[i]

        a, b = m1, m2  # Записываем старые центроиды
        m1 = sum1 / k  # Высчитываем новые центроиды
        m2 = sum2 / j
        flag = (m1 == a and m2 == b)  # Если оба значения центроида = старому => выйти из цикла

        print("\n____________ITERATION", m, "____________")
        print("m1=", m1, "m2=", m2)
        print("Cluster 1:\n", cluster1)
        print("Cluster 2:\n", cluster2)

    print("_____________________________")
    print("Final value of centorid: m1=", m1, "m2=", m2)
    print()
    print("Final cluster 1 is:\n", cluster1)
    print("Final cluster 2 is:\n", cluster2)


if __name__ == "__main__":
    main()
