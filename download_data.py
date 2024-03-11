from urllib import request, error
from datetime import datetime
import os


def download_vhi(region_index):
    url = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={region_index}&year1=1981&year2=2020&type=Mean'

    try:
        # Відкриваємо url та зчитуємо вміст
        with request.urlopen(url) as wp:
            text = wp.read()

        now = datetime.now()
        date_and_time = now.strftime("%d%m%Y%H%M%S")

        # Якщо не існує каталогу, то створюємо, щоб зберігати файли з даними
        if not os.path.exists('vhi_regions_data'):
            os.makedirs('vhi_regions_data')

        file = os.path.join('vhi_regions_data', f'vhi_data_region_{region_index}_{date_and_time}.csv')
        # Записуємо вміст у файл
        with open(file, 'wb') as out:
            out.write(text)

        print(
            f'VHI data for region {region_index} is downloaded and saved to {file}.')
    except error.HTTPError:
        print('Failed to download')


for i in range(1, 29):
    download_vhi(i)
