import pandas as pd


# 2. Пронормувати вибраний датасет або стандартизувати
def normalize_data(data):
    min_val = data.min()
    max_val = data.max()
    norm_data = (data - min_val) / (max_val - min_val)
    return norm_data


df = pd.read_csv('../info/wine.csv', sep=',')
print("Normalized DataFrame:", normalize_data(df), sep='\n')
