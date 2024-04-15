import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../info/wine.csv')

# 3. Збудувати гістограму по одному із атрибутів, що буде показувати на
# кількість елементів, що знаходяться у 10 діапазонах, які ви задасте.
plt.hist(df['Alcohol'], bins=10, edgecolor='black')
plt.title(f'Гістограма')
plt.xlabel('Алкоголь')
plt.ylabel('Частота')
plt.show()
