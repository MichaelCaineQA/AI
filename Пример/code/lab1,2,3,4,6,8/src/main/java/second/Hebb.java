package second;

import java.util.*;
import java.util.stream.Collectors;

import static java.lang.Math.abs;
import static java.util.Objects.*;

//Сигнальный метод обучения Хебба
public class Hebb {
    private final LinkedList<List<Neuron>> neuralNetwork;
    private final List<Synapse> synapses = new ArrayList<>();
    private final double a = 0.3;
    double trainingResult; // Ожидаемая активность выходного нейрона при полном соответствии образа

    public Hebb() {
        neuralNetwork = initNeuralNetwork();
        System.out.println("Neural Network is:");
        neuralNetwork.forEach(System.out::println);
    }

    private void setInput(int[] entry) {
        List<Neuron> i = neuralNetwork.getFirst();
        for (int idx = 0; idx < entry.length; idx++) {
            Neuron neuron = i.get(idx);
            neuron.setIn(entry[idx]); // Определяем вход нейрона
        }
    }

    public void train(int[] input) {
        System.out.println("Training neural network for image: " + Arrays.toString(input));
        setInput(input);
        for (int i = 1; i <= 1000; i++) {
            System.out.printf("====== ITERATION #%d ======%n", i);
            iterate();
            updateSynapses();
            if (i == 1000) {
                trainingResult = neuralNetwork.peekLast().get(0).out;
            }
            resetAllNeurons();
        }
    }

    private void resetAllNeurons() {
        // Обнуляем активность всех нейронов
        for (List<Neuron> neurons : neuralNetwork) {
            for (Neuron neuron : neurons) {
                neuron.out = 0;
            }
        }
    }

    private void updateSynapses() {
        // Обновить вес синапсов
        System.out.println("====== UPDATE SYNAPSES WEIGHT ======");
        for (Synapse synapse : synapses) {
            synapse.wIJ += a * synapse.neuronI.out * synapse.neuronJ.out;
            System.out.printf("====== CURRENT SYNAPSE (i): %s ======%n", synapse);
        }
    }

    public void iterate() {
        LinkedList<List<Neuron>> localNeuralNetwork = new LinkedList<>(neuralNetwork);
        List<Neuron> layer = localNeuralNetwork.poll();
        List<Neuron> nextLayer = localNeuralNetwork.poll();
        // Вычислить выходы слоя i, поставить их сумму на вход слою j
        while (nextLayer != null && layer != null) {
            for (Neuron neuronI : layer) {
                neuronI.out = 0; // Обнулить выход нейрона
                neuronI.getResult(); // Вычислить выход нейрона

                List<Synapse> neuronSynapses = synapses.stream() // Найти синапсы нейрона
                        .filter(s -> s.neuronI.equals(neuronI))
                        .collect(Collectors.toList());

                for (Synapse neuronSynapse : neuronSynapses) {
                    Neuron neuronJ = neuronSynapse.neuronJ;
                    neuronJ.in = neuronI.out; // Поставляем выход i на вход j
                    neuronJ.w = neuronSynapse.wIJ; // Ставим вес нейрону j = весу синапса
                    double out = neuronJ.out; // Сохраняем имеющийся выход нейрона j
                    out += neuronJ.getResult(); // Вычисляем выход нейрона j
                    neuronJ.out = out; // Обновляем значение выхода нейрона j
                }
            }
            layer = nextLayer;
            nextLayer = localNeuralNetwork.poll();
        }
    }

    public double getResult(int[] input) {
        setInput(input);
        iterate();
        System.out.println("Calculating result for: " + Arrays.toString(input));
        Neuron neuron = neuralNetwork.peekLast().get(0);
        System.out.println("Result neuron is: " + neuron);

        return neuron.out;
    }

    private LinkedList<List<Neuron>> initNeuralNetwork() {
        List<Neuron> i = new LinkedList<>();
        for (int idx = 0; idx < 3; idx++) { // Входной слой из 3 нейронов
            i.add(new Neuron("1." + idx));
        }

        List<Neuron> j = new LinkedList<>();
        for (int idx = 0; idx < 1; idx++) { // Промежуточный слой из 2 нейронов
            j.add(new Neuron("2." + idx));
        }
        i.forEach(neuron -> neuron.createSynapsesWithNextLayer(j, synapses)); // Создаём синапсы между нейронами 1 и 2 слоя

        return new LinkedList<List<Neuron>>() {{
            add(i);
            add(j);
        }};
    }

    public static void main(String[] args) {
        Hebb hebb = new Hebb();
        int[] originImage = new int[]{0, 1, 1};
        hebb.train(originImage);
        double trainingResult = hebb.getTrainingResult();
        int[] inputImage = new int[]{0, 0, 1};
        double result = hebb.getResult(inputImage);
        double eps = abs(trainingResult * 0.1);
        System.out.println("Actual result: " + result);
        System.out.println("Estimating result: " + trainingResult);
        if (abs(trainingResult - result) <= eps) {
            System.out.printf("Input image {%s} is similar to origin image {%s}%n", Arrays.toString(inputImage), Arrays.toString(originImage));
        } else {
            System.out.printf("Input image {%s} are different with origin image {%s}%n", Arrays.toString(inputImage), Arrays.toString(originImage));
        }
    }

    private double getTrainingResult() {
        return trainingResult;
    }

    static class Neuron {
        private final String name;
        private double w = new Random().nextDouble() * 0.3; // Начальный вес нейрона от 0 до 0.1
        private double in;
        private double out = 0;

        public Neuron(String name) {
            this.name = name;
        }

        public void setIn(double in) {
            this.in = in;
        }

        public double getW() {
            return w;
        }

        public void setW(double w) {
            this.w = w;
        }

        public void createSynapsesWithNextLayer(List<Neuron> nextLayer, List<Synapse> synapses) {
            for (Neuron nextNeuron : nextLayer) {
                synapses.add(new Synapse(this, nextNeuron, (new Random().nextDouble() + 0.1) * 0.3)); // Создаём синапсы между нейронами текущего и следующего слоя
            }
        }

        @Override
        public String toString() {
            return "Neuron{" +
                    "name=" + name +
                    ", w=" + w +
                    ", in=" + in +
                    ", out=" + out +
                    '}';
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Neuron neuron = (Neuron) o;
            return Objects.equals(name, neuron.name);
        }

        @Override
        public int hashCode() {
            return hash(name);
        }

        public double getResult() {
            this.out = this.in * this.w;

            return this.out;
        }
    }

    static class Synapse {
        private Neuron neuronI;
        private Neuron neuronJ;
        private Double wIJ;

        public Synapse(Neuron neuronI, Neuron neuronJ, Double wIJ) {
            this.neuronI = neuronI;
            this.neuronJ = neuronJ;
            this.wIJ = wIJ;
        }

        @Override
        public String toString() {
            return "Synapse{" +
                    "neuronI=" + neuronI.name +
                    ", neuronJ=" + neuronJ.name +
                    ", wIJ=" + wIJ +
                    '}';
        }
    }
}
