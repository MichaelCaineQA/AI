package third;

import java.io.*;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

public class Hopfield {
    public static void main(String[] args) {
        Shape input = ShapeParser.parse(INPUT_PATH).get(0);
        List<Shape> shapes = ShapeParser.parse(SHAPES_PATH);

        Hopfield hopfield = new Hopfield(input.size());
        for (Shape shape : shapes) {
            hopfield.trainNetwork(shape);
        }
        Shape recognizedShape = hopfield.recognize(input);
        System.out.println("Result: ");
        System.out.println(recognizedShape);
    }


    public static final String SHAPES_PATH = "src/main/resources/hopfield/shapes";
    public static final String INPUT_PATH = "src/main/resources/hopfield/input/modifiedK.txt";
    private List<Shape> shapes = new ArrayList<>(); // Известные сети образы
    private int[][] W; // Матрица нейронов
    private int n;

    public Hopfield(int n) {
        W = new int[n][n];
        this.n = n;
    }

    // Вычисление квадратной матрицы для ключевого образа
    public void trainNetwork(Shape shape) {
        shapes.add(shape);
        Integer[] X = shape.toIntegers();

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (i == j) {
                    W[i][j] = 0;
                } else {
                    W[i][j] += X[i] * X[j];
                }
            }
        }
    }

    public Shape recognize(Shape shape) {
        System.out.println("Known shapes: ");
        for (Shape knownShape : shapes) {
            System.out.println(knownShape);
        }

        System.out.println("Input shape: ");
        System.out.println(shape);

        Integer[] Y = shape.toIntegers();
        int maxTries = 200;
        int errs = 0;
        int iters = 0;
        Shape modifiedShape = shape;

        while (!shapes.contains(modifiedShape)) {
            iters++;
            boolean success = recstep(Y);
            modifiedShape = new Shape(Y);
            System.out.println("Modified shape: ");
            System.out.println(modifiedShape);
            if (success) {
                errs = 0;
            } else {
                errs++;
            }
            if (errs >= maxTries) {
                System.out.printf("Cannot recognize shape in %d iterations%n", iters);
                return modifiedShape;
            }
        }

        System.out.printf("Result found in %d iterations%n", iters);
        return modifiedShape;
    }

    private boolean recstep(Integer[] Y) {
        int r = (int) ((Math.random() * (Y.length)));
        int net = 0;
        for (int i = 0; i < Y.length; i++) {
            net += Y[i] * W[i][r];
        }
        System.out.println("net is " + net);
        int signet = Integer.compare(net, 0);
        System.out.println("signet is " + signet);
        System.out.println("Y[r] is " + Y[r]);
        if (signet != Y[r]) {
            System.out.printf("Neuron %d: %d -> %d%n", r, Y[r], signet);
            Y[r] = signet;

            return true;
        } else {
            return false;
        }
    }

    public static class Shape {
        private final List<List<ShapeChar>> lines;
        private final int size;

        public Shape(String shapeStr) {
            List<List<ShapeChar>> lines = new ArrayList<>();
            String[] linesStr = shapeStr.split("\n");
            for (String line : linesStr) {
                List<ShapeChar> lineChars = new ArrayList<>();
                for (char c : line.toCharArray()) {
                    lineChars.add(ShapeChar.getByChar(c));
                }
                lines.add(lineChars);
            }

            this.lines = lines;
            this.size = (int) Math.pow(lines.size(), 2);
        }

        public Shape(Integer[] Y) {
            List<List<ShapeChar>> lines = new ArrayList<>();
            int n = (int) Math.sqrt(Y.length);
            int j = 0;
            for (int i = 0; i < n; i++) {
                List<ShapeChar> line = new ArrayList<>();
                Integer[] lineInt = new Integer[n];
                System.arraycopy(Y, j, lineInt, 0, n);
                for (Integer intChar : lineInt) {
                    ShapeChar shapeChar = ShapeChar.getByInt(intChar);
                    line.add(shapeChar);
                }
                lines.add(line);
                j += n;
            }

            this.lines = lines;
            this.size = (int) Math.pow(lines.size(), 2);
        }

        public Integer[] toIntegers() {
            return lines.stream()
                    .map(line -> line.stream()
                            .map(ShapeChar::getIntVal)
                            .collect(Collectors.toList()))
                    .flatMap(Collection::stream)
                    .toArray(Integer[]::new);
        }

        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            for (List<ShapeChar> line : lines) {
                line.forEach(shapeChar -> sb.append(shapeChar.charVal));
                sb.append("\n");
            }
            return sb.toString();
        }

        public int size() {
            return size;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Shape shape = (Shape) o;
            return size == shape.size && Objects.equals(lines, shape.lines);
        }

        @Override
        public int hashCode() {
            return Objects.hash(lines, size);
        }
    }

    public enum ShapeChar {
        DASH('-', -1),
        AT('@', 1);

        private final char charVal;
        private final int intVal;

        ShapeChar(char val, int intVal) {
            this.charVal = val;
            this.intVal = intVal;
        }

        public int getIntVal() {
            return intVal;
        }

        public static ShapeChar getByInt(int intVal) {
            switch (intVal) {
                case 1:
                    return AT;
                case -1:
                    return DASH;
                default:
                    throw new IllegalArgumentException("Wrong ShapeChar int val: " + intVal);
            }
        }

        public static ShapeChar getByChar(char c) {
            switch (c) {
                case '-':
                    return DASH;
                case '@':
                    return AT;
                default:
                    throw new IllegalArgumentException("Wrong ShapeChar char val: " + c);
            }
        }
    }

    public static class ShapeParser {
        public static List<Shape> parse(String path) {
            List<Shape> result = new ArrayList<>();
            File files = new File(path);
            if (files.isDirectory()) {
                File[] listFiles = files.listFiles();
                for (File file : listFiles) {
                    String fileStr = read(file);
                    Shape shape = new Shape(fileStr);
                    result.add(shape);
                }
            } else {
                String fileStr = read(files);
                Shape shape = new Shape(fileStr);
                result.add(shape);
            }

            return result;
        }

        private static String read(File file) {
            try {
                FileInputStream fis = new FileInputStream(file);
                StringBuilder sb = new StringBuilder();
                try (BufferedReader reader = new BufferedReader(new InputStreamReader(fis))) {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        sb.append(line).append("\n");
                    }
                    return sb.toString();
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }
}
