import os
import csv
import requests
import pandas as pd
from zipfile import ZipFile, BadZipfile


# Завантажую та розархівовую архів
def get_and_extract_archive():
    try:
        zip_data = requests.get(
            'https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip'
        )

        with open('data.zip', 'wb') as archive:
            archive.write(zip_data.content)

        with ZipFile('data.zip', 'r') as data:
            data.extractall('../info')

        os.remove('data.zip')
    except BadZipfile as error:
        print(error)


# Конвертую в csv-формат
def convert_txt_to_csv():
    try:
        with open('../info/household_power_consumption.txt', 'r') as txt_file:
            with open('../info/household_power_consumption.csv', 'w') as csv_file:
                writer = csv.writer(csv_file)

                for each_line in txt_file:
                    values = each_line.strip().split(',')
                    writer.writerow(values)

        os.remove('../info/household_power_consumption.txt')
    except FileNotFoundError as error:
        print(error)


# Прибираю порожні значення
def remove_missing_values():
    try:
        df = pd.read_csv('../info/household_power_consumption.csv', sep=';')
        df = df.dropna()
        df.to_csv('../info/household_power_consumption.csv', index=False)
    except Exception as error:
        print(error)


get_and_extract_archive()
convert_txt_to_csv()
remove_missing_values()
