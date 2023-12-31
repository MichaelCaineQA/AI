import random


class Hebb:
    def __init__(self):
        self.weights = []
        self.learning_coff = 0.3
        self.training_result = 0  # Ожидаемая активность выходного нейрона при полном соответствии образа
        self.neural_network = self.init_neural_network()

    def init_neural_network(self):
        i = [Neuron(f"1.{idx}") for idx in range(3)]  # Входной слой из 3 нейронов
        j = [Neuron(f"2.{idx}") for idx in range(2)]  # Промежуточный слой из 2 нейронов
        for neuron_i in i:
            neuron_i.fill_weights(j, self.weights)  # Установление между ними весов
        return [i, j]

    def set_input(self, entry):
        for neuron_id, neuron in enumerate(self.neural_network[0]):
            neuron.set_in(entry[neuron_id])  # Определяем вход нейрона

    def train(self, input_data):
        print(f"Training neural network for image: {input_data}")
        self.set_input(input_data)
        epochs = 1000
        for i in range(epochs):
            if i % 100 == 0:
                print(f"Epoch №{i + 1}")
                print(f"Weights are:")
                for weight in self.weights:
                    print(f"{weight}")
            self.iterate()
            self.update_weights()
            if i == 999:
                self.training_result = self.neural_network[-1][0].out
            self.reset_all_neurons()

    # Обнуляем активность всех нейронов
    def reset_all_neurons(self):
        for layer in self.neural_network:
            for neuron in layer:
                neuron.out = 0

    # Обновить веса
    def update_weights(self):
        for weight in self.weights:
            weight.w_ij += self.learning_coff * weight.neuron_i.out * weight.neuron_j.out

    def iterate(self):
        local_neural_network = list(self.neural_network)
        layer = local_neural_network.pop(0)
        next_layer = local_neural_network.pop(0) if local_neural_network else None
        while next_layer is not None and layer is not None:
            for neuron_i in layer:
                neuron_i.out = 0
                neuron_i.get_result()
                neuron_weights = [weight for weight in self.weights if weight.neuron_i == neuron_i]
                # активационная функция
                for neuron_weight in neuron_weights:
                    neuron_j = neuron_weight.neuron_j
                    neuron_j.in_value = neuron_i.out
                    neuron_j.w = neuron_weight.w_ij
                    out = neuron_j.out
                    out += neuron_j.get_result()
                    neuron_j.out = out
            layer = next_layer
            next_layer = local_neural_network.pop(0) if local_neural_network else None

    def get_result(self, input_data):
        self.set_input(input_data)
        self.iterate()
        print(f"Calculating result for: {input_data}")
        neuron = self.neural_network[-1][0]
        print(f"Result neuron is: {neuron}")
        return neuron.out


    def get_training_result(self):
        return self.training_result


class Neuron:
    def __init__(self, name):
        self.name = name
        self.w = random.uniform(0, 0.1)  # Начальный вес нейрона от 0 до 0.1
        self.in_value = 0
        self.out = 0

    def set_in(self, in_value):
        self.in_value = in_value

    def fill_weights(self, next_layer, weights):
        for next_neuron in next_layer:
            weights.append(Weight(self, next_neuron, (random.uniform(0.1, 0.4) * 0.3)))

    def get_result(self):
        self.out = self.in_value * self.w
        return self.out


class Weight:
    def __init__(self, neuron_i, neuron_j, w_ij):
        self.neuron_i = neuron_i
        self.neuron_j = neuron_j
        self.w_ij = w_ij

    def __str__(self):
        return f"neuron I = {self.neuron_i.name}, neuronJ={self.neuron_j.name}, wIJ={self.w_ij}"


if __name__ == "__main__":
    hebb = Hebb()
    origin_image = [0, 1, 1]
    hebb.train(origin_image)
    training_result = hebb.get_training_result()
    input_image = [0, 1, 1]
    result = hebb.get_result(input_image)
    eps = abs(training_result * 0.1)
    print(f"Actual result: {result}")
    print(f"Estimating result: {training_result}")
    if abs(training_result - result) <= eps:
        print(f"Input image {input_image} is similar to origin image {origin_image}")
    else:
        print(f"Input image {input_image} are different with origin image {origin_image}")
