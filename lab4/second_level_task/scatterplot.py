import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../info/wine.csv')

# 4. Збудувати графік залежності одного integer/real атрибута від іншого.
plt.scatter(df['Alcohol'], df['Malicacid'], alpha=0.5)
plt.title('Графік залежності від алкоголю до яблучної кислоти')
plt.xlabel('Алкоголь')
plt.ylabel('Яблучна кислота')
plt.show()
