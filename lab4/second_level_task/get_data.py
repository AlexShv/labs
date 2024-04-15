from ucimlrepo import fetch_ucirepo
import pandas as pd


# Видаляю значення, там де пусті дані
def handle_missing_values(df):
    df.dropna(inplace=True)
    return df


# Завантажую датасет
wine = fetch_ucirepo(id=109)

X = wine.data.features
X_df = pd.DataFrame(X)

X_df_processed = handle_missing_values(X_df)
X_df_processed.to_csv('info/wine.csv', index=False)
print(X_df_processed)
