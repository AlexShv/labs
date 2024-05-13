import numpy as np
import matplotlib.pyplot as plt


def linear_regression_gradient_descent(X, Y, learning_rate=0.01, n_iter=1000):
    k = np.random.uniform(-1, 1)
    b = np.random.uniform(-1, 1)
    mse_history = []

    for _ in range(n_iter):
        k_grad = -(2 / len(X)) * np.sum(X * (Y - (k * X + b)))
        b_grad = -(2 / len(X)) * np.sum(Y - (k * X + b))

        k_new = k - learning_rate * k_grad
        b_new = b - learning_rate * b_grad

        k = k_new
        b = b_new

        # Обчислення середньоквадратичної помилки (MSE)
        mse = np.mean((Y - (k * X + b)) ** 2)
        mse_history.append(mse)

    return k, b, mse_history


k, b = 2, 3
X = np.random.uniform(0, 10, 100)
noise = np.random.normal(0, 1, 100)
n_iter=1000
Y = k * X + b + noise

opt_k, opt_b, mse_history = linear_regression_gradient_descent(X, Y)

print("Оптимальний нахил (k):", opt_k)
print("Оптимальне зміщення (b):", opt_b)


# Функція для обчислення лінії регресії
def regression_line(X, k, b):
    return k * X + b


plt.figure(figsize=(12, 5))

# Графік даних
plt.subplot(1, 2, 1)
plt.scatter(X, Y, color='blue', label='Дані')
plt.plot(X, regression_line(X, opt_k, opt_b), color='red', label='Лінія регресії')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Лінійна регресія з градієнтним спуском')
plt.legend()
plt.grid(True)

# Графік похибки
plt.subplot(1, 2, 2)
plt.plot(range(1, n_iter + 1), mse_history)
plt.xlabel('Кількість ітерацій')
plt.ylabel('Середньоквадратична помилка (MSE)')
plt.title('Залежність помилки від кількості ітерацій')
plt.grid(True)

plt.tight_layout()
plt.show()
