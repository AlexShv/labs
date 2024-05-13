import numpy as np
import matplotlib.pyplot as plt


# Завдання 1: Генерація двовимірних даних
k, b = 2, 3

x = np.random.uniform(0, 10, 100)

noise = np.random.normal(0, 1, 100)

y = k * x + b + noise


# Завдання 2: Реалізація методу найменших квадратів для пошуку оптимальних оцінок
def least_squares(x, y):
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    xy_mean = np.mean(x * y)
    x_squared_mean = np.mean(x**2)

    # Обчислення параметрів прямої регресії
    k_res = (xy_mean - x_mean * y_mean) / (x_squared_mean - x_mean ** 2)
    b_res = y_mean - k_res * x_mean

    return k_res, b_res


# Завдання 3: Порівняння знайдених параметрів
k_hat, b_hat = least_squares(x, y)
k_np, b_np = np.polyfit(x, y, 1)

print("Оцінки параметрів за допомогою реалізованої функції:")
print("k_hat:", k_hat)
print("b_hat:", b_hat)
print("\nОцінки параметрів за допомогою numpy.polyfit:")
print("k_np:", k_np)
print("b_np:", b_np)


# Завдання 4: Відображення результатів на графіку
plt.figure(figsize=(12, 8))

plt.scatter(x, y, label='Дані')
plt.plot(x, k_hat * x + b_hat, color='red', label='Оцінка (реалізація)')
plt.plot(x, k_np * x + b_np, color='green', label='Оцінка (numpy)')
plt.plot(x, k * x + b, color='blue', label='Справжня пряма')
plt.legend()
plt.xlabel('Вісь OX')
plt.ylabel('Вісь OY')
plt.title('Оцінка лінії регресії')
plt.grid(True)
plt.show()
