package fourth;

import third.Hopfield.Shape;

import java.util.Arrays;
import java.util.List;

import static third.Hopfield.INPUT_PATH;
import static third.Hopfield.SHAPES_PATH;
import static third.Hopfield.ShapeParser.*;

public class PotentialMethod {
    public static void main(String[] args) {
        PotentialMethod potentialMethod = new PotentialMethod();
        potentialMethod.potential();
        Shape result = potentialMethod.getResult();
        System.out.println("Result: ");
        System.out.println(result);
    }

    List<Shape> shapes = parse(SHAPES_PATH);
    Shape input = parse(INPUT_PATH).get(0);
    double[] Ps = new double[shapes.size()];

    public Shape getResult() {
        System.out.println("Input: ");
        System.out.println(input);

        // Найти наибольший потенциал
        double maxP = -1;
        int idxMaxP = -1;
        for (int i = 0; i < Ps.length; i++) {
            double p = Ps[i];
            if (p > maxP) {
                maxP = p;
                idxMaxP = i;
            }
        }

        return shapes.get(idxMaxP);
    }

    /**
     * Метод вычисления потенциалов для каждой фигуры
     */
    public void potential() {
        for (int i = 0; i < shapes.size(); i++) {
            Shape shape = shapes.get(i);
            int r = compare(input, shape);
            Ps[i] += 1_000_000 / (1 + Math.pow(r, 2));
        }

        System.out.println("Potentials: ");
        System.out.println(Arrays.toString(Ps));
    }


    /**
     * Метод вычисления расстояния до эталонного рисунка (расстояния по Хэммингу)
     *
     * @param b1 входное изображение
     * @param b2 эталонное изображение для сравнения
     */
    private int compare(Shape b1, Shape b2) {
        int count = 0;
        assert b1.size() == b2.size(); // Размеры сравниваемых фигур равны
        int n = b1.size();
        int[][] b1Pixels = toPixels(b1);
        int[][] b2Pixels = toPixels(b2);

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (b1Pixels[i][j] != b2Pixels[i][j]) {
                    count++;
                }
            }
        }

        return count;
    }

    private int[][] toPixels(Shape shape) {
        int[][] result = new int[shape.size()][shape.size()];
        Integer[] Y = shape.toIntegers();
        int n = (int) Math.sqrt(Y.length);
        int k = 0;
        for (int i = 0; i < n; i++) {
            Integer[] lineInt = new Integer[n];
            System.arraycopy(Y, k, lineInt, 0, n);
            for (int j = 0; j < lineInt.length; j++) {
                Integer intChar = lineInt[j];
                result[i][j] = intChar;
            }
            k += n;
        }

        return result;
    }

}
