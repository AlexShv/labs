import pandas as pd
import matplotlib.pyplot as plt

# Провести візуалізацію багатовимірних даних, використовуючи приклади, наведені у медіумі
df = pd.read_csv('../info/wine.csv')

xs = df['Alcohol']
ys = df['Malicacid']
zs = df['Ash']

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(xs, ys, zs, s=50, alpha=0.6, edgecolors='w')

ax.set_xlabel('Alcohol')
ax.set_ylabel('Malicacid')
ax.set_zlabel('Ash')

plt.show()
