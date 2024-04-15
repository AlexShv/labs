import pandas as pd
import numpy as np
from timeit import timeit


# 1. Обрати всі домогосподарства, у яких загальна активна споживана потужність перевищує 5 кВт
def task_1_pd(data):
    houses_over_5kW = data[data['Global_active_power'] > 5]
    return houses_over_5kW


def task_1_np(data):
    global_active_power = data[:, 2].astype(float)
    houses_over_5kW = data[global_active_power > 5]
    return houses_over_5kW


# 2. Обрати всі домогосподарства, у яких вольтаж перевищую 235 В.
def task_2_pd(data):
    houses_with_high_voltage = data[data['Voltage'] > 235]
    return houses_with_high_voltage


def task_2_np(data):
    voltage = data[:, 4].astype(float)
    houses_with_high_voltage = data[voltage > 235]
    return houses_with_high_voltage


# 3. Обрати всі домогосподарства, у яких сила струму лежить в межах
# 19-20 А, для них виявити ті, у яких пральна машина та холодильних
# споживають більше, ніж бойлер та кондиціонер.
def task_3_pd(data):
    houses_19_20A = data[(data['Global_intensity'] >= 19) & (data['Global_intensity'] <= 20)]
    selected_houses = houses_19_20A[houses_19_20A['Sub_metering_2'] > houses_19_20A['Sub_metering_3']]
    return selected_houses


def task_3_np(data):
    global_intensity = data[:, 5].astype(float)
    houses_19_20A = data[(global_intensity >= 19) & (global_intensity <= 20)]
    selected_houses = houses_19_20A[houses_19_20A[:, 7] > houses_19_20A[:, 8]]
    return selected_houses


# 4. Обрати випадковим чином 500000 домогосподарств (без повторів
# елементів вибірки), для них обчислити середні величини усіх 3-х
# груп споживання електричної енергії
def task_4_pd(data):
    random_houses = data.sample(n=500000)
    avg_consumptions = random_houses[['Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']].astype(float).mean()
    return avg_consumptions


def task_4_np(data):
    random_indices = np.random.randint(0, len(data), size=500000)
    random_houses = data[random_indices]
    avg_consumptions = np.mean(random_houses[:, 6:9].astype(float), axis=0)
    return avg_consumptions


# 5. Обрати ті домогосподарства, які після 18-00 споживають понад 6
# кВт за хвилину в середньому, серед відібраних визначити ті, у яких
# основне споживання електроенергії у вказаний проміжок часу
# припадає на пральну машину, сушарку, холодильник та освітлення
# (група 2 є найбільшою), а потім обрати кожен третій результат із
# першої половини та кожен четвертий результат із другої половини.
def task_5_pd(data):
    data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

    # Фільтруємо дані для домогосподарств, які споживають понад 6 кВт після 18:00
    filtered_households = data[
        (data['Datetime'].dt.hour >= 18) &
        (data.groupby('Datetime')['Global_active_power'].transform('mean') > 6) &
        ((data['Sub_metering_1'] + data['Sub_metering_2'] + data['Sub_metering_3']) > 6)
        ]

    result = filtered_households.iloc[::3, :]
    result = pd.concat([result, filtered_households.iloc[len(result):, :].iloc[::4, :]])

    return result


data_df = pd.read_csv('../info/household_power_consumption.csv', sep=',')
data_np = np.genfromtxt('../info/household_power_consumption.csv', delimiter=',', skip_header=1, dtype=str)


# 1. Обрати всі домогосподарства, у яких загальна активна споживана потужність перевищує 5 кВт
print("1. Домогосподарства зі споживанням понад 5 кВт:")
print('Pandas Dataframe:', task_1_pd(data_df), timeit(stmt='task_1_pd(data_df)', globals=globals(), number=1), sep='\n')
print('Numpy Array:', task_1_np(data_np), timeit(stmt='task_1_np(data_np)', globals=globals(), number=1), sep='\n')
print('-'*70)


# 2. Обрати всі домогосподарства, у яких вольтаж перевищую 235 В.
print("2. Домогосподарства, у яких вольтаж перевищую 235 В:")
print('Pandas Dataframe:', task_2_pd(data_df), timeit(stmt='task_2_pd(data_df)', globals=globals(), number=1), sep='\n')
print('Numpy Array:', task_2_np(data_np), timeit(stmt='task_2_np(data_np)', globals=globals(), number=1), sep='\n')
print('-'*70)


# 3. Обрати всі домогосподарства, у яких сила струму лежить в межах
# 19-20 А, для них виявити ті, у яких пральна машина та холодильних
# споживають більше, ніж бойлер та кондиціонер.
print("3. Обрати всі домогосподарства, у яких сила струму лежить в межах 19-20 А:")
print('Pandas Dataframe:', task_3_pd(data_df), timeit(stmt='task_3_pd(data_df)', globals=globals(), number=1), sep='\n')
print('Numpy Array:', task_3_np(data_np), timeit(stmt='task_3_np(data_np)', globals=globals(), number=1), sep='\n')
print('-'*70)


# 4. Обрати випадковим чином 500000 домогосподарств (без повторів
# елементів вибірки), для них обчислити середні величини усіх 3-х
# груп споживання електричної енергії
print("4. Обчислити середні величини усіх 3-х груп споживання електричної енергії:")
print('Pandas Dataframe:', task_4_pd(data_df), timeit(stmt='task_4_pd(data_df)', globals=globals(), number=1), sep='\n')
print('Numpy Array:', task_4_np(data_np), timeit(stmt='task_4_np(data_np)', globals=globals(), number=1), sep='\n')
print('-'*70)


# 5. Обрати ті домогосподарства, які після 18-00 споживають понад 6
# кВт за хвилину в середньому, серед відібраних визначити ті, у яких
# основне споживання електроенергії у вказаний проміжок часу
# припадає на пральну машину, сушарку, холодильник та освітлення
# (група 2 є найбільшою), а потім обрати кожен третій результат із
# першої половини та кожен четвертий результат із другої половини.
print("5. Обрати ті домогосподарства, які після 18-00 споживають понад 6 кВт за хвилину в середньому:")
print('Pandas Dataframe:', task_5_pd(data_df), timeit(stmt='task_5_pd(data_df)', globals=globals(), number=1), sep='\n')
print('-'*70)
