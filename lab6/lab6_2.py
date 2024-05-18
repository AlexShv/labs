import numpy as np
import matplotlib.pyplot as plt


def linear_regression_gradient_descent(X, Y, learning_rate=0.01, stopping_criteria=1e-6, max_iter=10000):
    k = np.random.uniform(-1, 1)
    b = np.random.uniform(-1, 1)
    mse_history = []

    for i in range(max_iter):
        k_grad = -(2 / len(X)) * np.sum(X * (Y - (k * X + b)))
        b_grad = -(2 / len(X)) * np.sum(Y - (k * X + b))

        k -= learning_rate * k_grad
        b -= learning_rate * b_grad

        # Обчислення MSE
        mse = np.mean((Y - (k * X + b)) ** 2)
        mse_history.append(mse)

        # Перевірка умови зупинки
        # порівнює різницю між значеннями MSE на двох послідовних ітераціях
        # яккщо ця різниця менша за stopping_criteria, то алгоритм припиняє свою роботу
        # при досягненні умови зупинки програма виводить повідомлення з номером ітерації,
        # на якій була досягнута умова зупинки
        if i > 0 and abs(mse_history[-2] - mse_history[-1]) < stopping_criteria:
            print(f"Зупинка на ітерації {i+1} через досягнення умови зупинки по MSE")
            break

    return k, b, mse_history


k_true, b_true = 2, 3
X = np.random.uniform(0, 10, 100)
noise = np.random.normal(0, 1, 100)
Y = k_true * X + b_true + noise

opt_k, opt_b, mse_history = linear_regression_gradient_descent(X, Y)

print("Оптимальний нахил (k):", opt_k)
print("Оптимальне зміщення (b):", opt_b)


# Функція для обчислення лінії регресії
def regression_line(X, k, b):
    return k * X + b


# Відображення результатів на графіку
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.scatter(X, Y, color='blue', label='Дані')
plt.plot(X, regression_line(X, opt_k, opt_b), color='red', label='Лінія регресії (градієнтний спуск)')
plt.plot(X, regression_line(X, k_true, b_true), color='green', label='Справжня лінія')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Лінійна регресія з градієнтним спуском')
plt.legend()
plt.grid(True)

# Графік похибки
plt.subplot(1, 2, 2)
plt.plot(range(1, len(mse_history) + 1), mse_history)
plt.xlabel('Кількість ітерацій')
plt.ylabel('Середньоквадратична помилка (MSE)')
plt.title('Залежність помилки від кількості ітерацій')
plt.grid(True)

plt.tight_layout()
plt.show()
