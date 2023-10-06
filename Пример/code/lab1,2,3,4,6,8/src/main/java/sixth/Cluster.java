package sixth;

import java.util.Arrays;

public class Cluster {
    public static void main(String[] args) {
        int[] arr = {2, 4, 10, 12, 3, 20, 30, 11, 25};
        System.out.println("Input: " + Arrays.toString(arr));
        int i, m1, m2, m = 0; //значение центроидов, m - число иттераций
        boolean flag; // флаг, который даст знать, что центры масс m1, m2 не меняются
        int sum1, sum2; // суммы одномерных массивов
        int a = arr[0];
        int b = arr[1]; //a, b сохраняют предыдущее состояние центра масс, чтобы сравнить с текущим значением
        m1 = a;
        m2 = b;
        int[] cluster1, cluster2;
        do {
            sum1 = 0;
            sum2 = 0;
            cluster1 = new int[arr.length];
            cluster2 = new int[arr.length];
            m++; //подсчет числа итераций
            int k = 0, j = 0; //элементы, которые будут записывать значения в первый и второй массив
            for (i = 0; i < arr.length; i++) {
                if (Math.abs(arr[i] - m1) <= Math.abs(arr[i] - m2)) { //принимаем за первую центроиду первое значение массива, за вторую - второе и сравниваем
                    cluster1[k] = arr[i]; //если проходит, то записываем в первый кластер
                    k++;
                } else {
                    cluster2[j] = arr[i];
                    j++;
                }
            }
            for (i = 0; i < k; i++) { //вычисляем сумму для 1го кластера
                sum1 += cluster1[i];
            }
            for (i = 0; i < j; i++) { //вычисляем сумму для 2го кластера
                sum2 += cluster2[i];
            }
            a = m1; //записываем старые центроиды
            b = m2;
            m1 = sum1 / k; //высчитываем новые центроиды
            m2 = sum2 / j;
            flag = (m1 == a && m2 == b); //если оба значения центроида = старому => выйти из цикла
            System.out.printf("%n____________ITERATION %d____________%n", m);
            System.out.println("m1=" + m1 + " m2=" + m2);
            System.out.println("Cluster 1:\n" + Arrays.toString(cluster1));
            System.out.println("Cluster 2:\n" + Arrays.toString(cluster2));
        } while (!flag);
        System.out.println("_____________________________");
        System.out.println("Final value of centorid: m1=" + m1 + " m2=" + m2);
        System.out.println();
        System.out.println("Final cluster 1 is:\n" + Arrays.toString(cluster1));
        System.out.println("Final cluster 2 is:\n" + Arrays.toString(cluster2));
    }
}
