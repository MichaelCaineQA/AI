import numpy as np
import matplotlib.pyplot as plt

import utils


# Сигмоида
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# Сгенерировать матрицу весов
def generate_weights(size_x, size_y):
    return np.random.uniform(-0.5, 0.5, (size_x, size_y))


# Алгоритм прямого распространения
def forward_propagation(input_data, weights, bias):
    raw_results = (weights @ input_data) + bias
    return sigmoid(raw_results)


# Собираем изображения и результаты
images, labels = utils.load_dataset()

# Веса и нейроны смещения
weights_input_to_hidden = generate_weights(20, 784)
weights_hidden_to_output = generate_weights(10, 20)
bias_input_to_hidden = np.zeros((20, 1))
bias_hidden_to_output = np.zeros((10, 1))

epochs = 3  # эпохи
e_loss = 0
e_correct = 0
learning_rate = 0.01

for epoch in range(epochs):
    print(f"Эпоха №{epoch + 1}")

    # По каждому изображению
    for image, label in zip(images, labels):
        image = np.reshape(image, (-1, 1))
        label = np.reshape(label, (-1, 1))

        # Проходим до скрытого слоя
        hidden = forward_propagation(image, weights_input_to_hidden, bias_input_to_hidden)

        # Проходим до выходного слоя
        output = forward_propagation(hidden, weights_hidden_to_output, bias_hidden_to_output)

        # Считаем потери и точность нейросети с ожидаемым результатом (MSE)
        e_loss += 1 / len(output) * np.sum((output - label) ** 2, axis=0)
        e_correct += int(np.argmax(output) == np.argmax(label))
        # метод наименьших квадратов?
        """
        Метод наименьших квадратов - это математический метод, который используется для нахождения наилучшей
        аппроксимирующей функции, которая минимизирует сумму квадратов разностей между наблюдаемыми значениями 
        и значениями функции.
        
        Формула метода наименьших квадратов используется для нахождения оптимальных значений параметров модели. 
        Пусть у нас есть набор наблюдаемых величин (x, y), где x - независимая переменная, 
        y - зависимая переменная. 
        Мы хотим найти аппроксимирующую функцию вида y = f(x, β), 
        где β - параметры модели, так чтобы минимизировать сумму квадратов ошибок (SSE):

        SSE = Σ(y - f(x, β))^2

        Для нахождения оптимальных значений параметров β минимизируется SSE 
        путем дифференцирования по параметрам и приравнивания производных к нулю. 
        Таким образом, система уравнений, которую нужно решить, имеет вид:
        
        ∂SSE/∂β = 0
    
        Решение этой системы уравнений дает оптимальные значения параметров модели,
         которые минимизируют сумму квадратов ошибок.
        """



        # Обратное распространение (до скрытого слоя)
        delta_output = output - label
        weights_hidden_to_output += -learning_rate * delta_output @ np.transpose(hidden)
        bias_hidden_to_output += -learning_rate * delta_output

        # Обратное распространение (до входного слоя)
        delta_hidden = np.transpose(weights_hidden_to_output) @ delta_output * (hidden * (1 - hidden))
        weights_input_to_hidden += -learning_rate * delta_hidden @ np.transpose(image)
        bias_input_to_hidden += -learning_rate * delta_hidden

    # Выводим потери и точность нейросети между эпохами
    print(f"Loss: {round((e_loss[0] / images.shape[0]) * 100, 3)}%")
    print(f"Accuracy: {round((e_correct / images.shape[0]) * 100, 3)}%")
    e_loss = 0.0
    e_correct = 0.0

# Проверка на реальном изображении
img = plt.imread("7.jpg", format="jpeg")

# Перекрашиваем изображение в чёрно-белое
gray = lambda rgb: np.dot(rgb[..., :3], [0.299, 0.587, 0.114])
img = 1 - (gray(img).astype("float32") / 255)

img = np.reshape(img, (img.shape[0] * img.shape[1]))
image = np.reshape(img, (-1, 1))

# Проходим до скрытого слоя
hidden = forward_propagation(image, weights_input_to_hidden, bias_input_to_hidden)

# Проходим до выходного слоя
output = forward_propagation(hidden, weights_hidden_to_output, bias_hidden_to_output)

# Показываем начальное изображение и предположение нейросети
plt.imshow(img.reshape(28, 28), cmap="Greys")
plt.title(f"Я думаю, что число на картинке это: {output.argmax()}")
plt.show()
