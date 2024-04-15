import pandas as pd
from scipy.stats import pearsonr, spearmanr

df = pd.read_csv('../info/wine.csv')

# 5. Підрахувати коефіцієнт Пірсона та Спірмена для двох integer/real атрибутів.
pearson_corr, _ = pearsonr(df['Total_phenols'], df['Color_intensity'])
print('Коефіцієнт Пірсона: ', pearson_corr)

spearman_corr, _ = spearmanr(df['Total_phenols'], df['Color_intensity'])
print('Коефіцієнт Спірмена: ', spearman_corr)
