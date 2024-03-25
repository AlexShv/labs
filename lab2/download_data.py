from urllib import request, error
from datetime import datetime
import os

# Створив словник, де вказав ключі(оригінальні значення), а значення -
# виправлені індекси
corrected_indices = {
    1: 22, 2: 24, 3: 23, 4: 25, 5: 3,
    6: 4, 7: 8, 8: 19, 9: 20, 10: 21,
    11: 9, 12: 9, 13: 10, 14: 11, 15: 12,
    16: 13, 17: 14, 18: 15, 19: 16, 20: 25,
    21: 17, 22: 18, 23: 6, 24: 1, 25: 2,
    26: 7, 27: 5
}


def download_vhi(region_index):
    # Для кожної області визначаю правильний індекс
    corrected_index = corrected_indices.get(region_index)

    url = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={region_index}&year1=1981&year2=2025&type=Mean'

    try:
        # Відкриваємо url та зчитуємо вміст
        with request.urlopen(url) as wp:
            text = wp.read()

        # Отримую поточний час та форматую його в спецільний формат,
        # щоб вказати в імені файлів
        now = datetime.now()
        date_and_time = now.strftime("%Y%m%d%H%M%S")

        # Якщо не існує каталогу, то створюємо, щоб зберігати файли з даними
        if not os.path.exists('vhi_regions_data'):
            os.makedirs('vhi_regions_data')

        # Створюємо назву файлу та записую вміст у файл
        file = os.path.join(
            'vhi_regions_data',
            f'vhi_data_region_{corrected_index}_{date_and_time}.csv'
        )
        with open(file, 'wb') as out:
            out.write(text)

        print(
            f'VHI data for region {corrected_index} is downloaded and saved to {file}.')
    except error.HTTPError:
        print(f'Failed to download data for region {corrected_index}.')


for i in range(1, 28):
    download_vhi(i)
