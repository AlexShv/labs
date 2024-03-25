import pandas as pd


# Пошук мінімального та максимального значення VHI для конкретної області та року
def find_extremes_for_region(dataframe, region, year):
    # Визначає підфрейм за значеннями стовпців Року та Регіону
    region_data = dataframe[(dataframe['Region_Index'] == region) & (dataframe['Year'] == year)]
    min_vhi_value = region_data['VHI'].min()
    max_vhi_value = region_data['VHI'].max()
    return min_vhi_value, max_vhi_value


# Для пошуку мінімального та максимального значення VHI для вказаного діапазону років та обраних областей
def find_extremes_for_years(dataframe, start_year, end_year, regions):
    result = []
    for region in regions:
        for year in range(start_year, end_year + 1):
            min_vhi_value, max_vhi_value = find_extremes_for_region(dataframe, region, year)
            result.append({'Region_Index': region, 'Year': year, 'Min VHI': min_vhi_value, 'Max VHI': max_vhi_value})
    return result


# Функція для знаходження років з екстремальними посухами
def find_drought_years(dataframe, threshold_percentage):
    total_regions = dataframe['Region_Index'].nunique()
    threshold_regions = int(threshold_percentage * total_regions / 100)

    drought_years = []
    for year in dataframe['Year'].unique():
        extreme_drought_count = dataframe[(dataframe['Year'] == year) & (dataframe['VHI'] < 15)].shape[0]
        if extreme_drought_count >= threshold_regions:
            drought_years.append(year)
    return drought_years


# Знаходження років з помірними посухами
def find_moderate_drought_years(dataframe, threshold_percentage):
    total_regions = dataframe['Region_Index'].nunique()
    threshold_regions = int(threshold_percentage * total_regions / 100)

    mod_drought_years = []
    for year in dataframe['Year'].unique():
        moderate_drought_count = dataframe[(dataframe['Year'] == year) & (dataframe['VHI'] < 35)].shape[0]
        if moderate_drought_count >= threshold_regions:
            mod_drought_years.append(year)
    return mod_drought_years


df = pd.read_csv('../lab3/data.csv')

for i in range(1, 26):
    min_vhi, max_vhi = find_extremes_for_region(df, region=i, year=1982)
    print(f"Min VHI для регіону з ID {i} у 1982: {min_vhi}, Max VHI для регіону з ID {i} у 1982: {max_vhi}")


extremes_result = find_extremes_for_years(df, start_year=1982, end_year=1983, regions=[1, 2, 3])
print("\nЕкстремальні значення VHI для вказаних років та регіонів:")
print(pd.DataFrame(extremes_result))


extreme_drought_years = find_drought_years(df, threshold_percentage=20)
print(f"\nРоки з екстремальними посухами: {extreme_drought_years}")


moderate_drought_years = find_moderate_drought_years(df, threshold_percentage=20)
print(f"Роки з помірними посухами: {moderate_drought_years}")
