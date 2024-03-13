import pandas as pd
import os


def read_files_to_dataframe(directory_path, output_file_path):
    # Визначаємо назви колонок та створюємо порожій DataFrame з ними
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'Region_Index', 'empty']
    dataframe = pd.DataFrame(columns=headers)

    # Проходимо по всіх CSV-файлах у заданій директорії
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            try:
                # Зчитуємо дані з CSV-файлу, пропускаючи перші два рядки та вказуючи назви колонок
                # Також прибрав табличні теги за допомогою str.replace
                df = pd.read_csv(file_path, skiprows=2, names=headers[:-1])
                df['Year'] = df['Year'].str.replace('<tt><pre>', '').str.replace('</pre></tt>', '')

                # Визначив індекс регіону з імені файлу та додаємо його до DataFrame
                region_index = int(filename.split('_')[3])
                df['Region_Index'] = region_index

                # Об'єднуємо DataFrame кожного файлу з загальним DataFrame
                dataframe = pd.concat([dataframe, df], ignore_index=True)
                print(f'Successfully read file: {filename}')
            except pd.errors.ParserError:
                print(f'Error reading {filename}: ParserError')

    dataframe.to_csv(output_file_path, index=False)
    print(f'DataFrame saved to: {output_file_path}')
    return dataframe


read_files_to_dataframe('vhi_regions_data', 'data.csv')
