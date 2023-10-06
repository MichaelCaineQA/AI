package first;

import java.util.Arrays;

import static java.util.Arrays.copyOf;

// Однонейронный перцептрон с двумя входами
public class Perceptron {
    double[] entries; // Входы
    double result; // Выход
    double[] weights; // Весовые коэф.
    double wk = 0.1; // Коэф. обучения

    // Логическое "ИЛИ"
    double[][] learnPatterns = { // Шаблоны обучения
            {0,0, 0}, // {Вход, Вход, Ожидаемый Выход}
            {0,1, 1},
            {1,0, 1},
            {1,1, 1}
    };

    public Perceptron() {
        this.entries = new double[2];
        this.weights = new double[entries.length];

        for (int i = 0; i < weights.length; i++) {
            weights[i] = Math.random() * 0.2 + wk;
        }
    }

    /**
     * Функция вычисления выхода нейрона
     */
    public void calculateResult() {
        result = 0;
        for (int i = 0; i < entries.length; i++) {
            result += entries[i] * weights[i]; // Передаём уровень активности входных нейронов по весовому коэфу на выходной нейрон
        }

        result = result > 0.5 ? 1 : 0; // Определяем преодолён ли порог для активации нейрона
    }

    /**
     * Обучение перцептрона.
     * Принцип: изменением весов в зависимости от ошибки до тех пор, пока ошибка не станет приемлемой
     * (не станет равно нулю в нашем случае)
     */
    public int learn() {
        double globalErr;
        int iterations = 0;
        do { // Обучаем  до тех пор, пока глобальная ошибка больше 0
            globalErr = 0;
            iterations++;
            for (double[] learnPattern : learnPatterns) {
                entries = copyOf(learnPattern, learnPattern.length - 1); // Входами стали элементы шаблона обучения (без последнего)
                calculateResult();
                double localErr = learnPattern[2] - result; // Считаем отклонение полученного результата от идеального из шаблона обучения
                globalErr += Math.abs(localErr);
                for (int i = 0; i < entries.length; i++) {
                    weights[i] += wk * localErr * entries[i];
                }
            }
        } while (globalErr > 0);

        return iterations;
    }

    public void test() {
        int iterations = learn();
        System.out.printf("Perceptron trained in %d iterations%n", iterations);
        for (double[] learnPattern : learnPatterns) {
            entries = copyOf(learnPattern, learnPattern.length - 1);
            System.out.printf("Input: %s%n", Arrays.toString(entries));
            calculateResult();
            System.out.printf("Result: %f%n", result);
        }
    }

    public static void main(String[] args) {
        new Perceptron().test();
    }
}
