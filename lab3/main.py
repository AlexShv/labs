from spyre import server
import pandas as pd


class SimpleApp(server.App):
    title = 'NOAA data visualization'

    regions_df = pd.read_csv('regions.csv')
    regions_list = regions_df['Region_Name'].tolist()

    inputs = [
        # Випадаючий список для вибору типу даних NOAA
        {
            'type': 'dropdown',
            'label': 'NOAA data',
            'options': [
                {'label': 'VCI', 'value': 'VCI'},
                {'label': 'TCI', 'value': 'TCI'},
                {'label': 'VHI', 'value': 'VHI'},
            ],
            'key': 'ticker',
            'action_id': 'update_data',
        },
        # Список вибору регіонів
        {
            'type': 'dropdown',
            'label': 'Region',
            'options': [{'label': region.split('_')[0], 'value': region.split('_')[1]} for region in regions_list],
            'key': 'region',
            'action_id': 'update_data',
        },
        # Текстове поле для введення діапазону місяців
        {
            'type': 'text',
            'label': 'Months interval:',
            'value': '1-12',
            'key': 'months_interval',
            'action_id': 'update_data',
        },
        # Список для вибору року
        {
            'type': 'dropdown',
            'label': 'Year',
            'options': [{'label': str(year), 'value': str(year)} for year in range(1982, 2025)],
            'key': 'year',
            'action_id': 'update_data'
        },
    ]

    controls = [{'type': 'button', 'label': 'Build plot', 'id': 'update_data'}]

    tabs = ['Plot']

    outputs = [
        # Відображення графіку
        {
            'type': 'plot',
            'id': 'plot_id',
            'control_id': 'update_data',
            'tab': 'Plot',
        },
    ]

    # Завантажую дані із CSV-файлу
    def getData(self, params):
        data = pd.read_csv('data.csv')
        return data

    # У цій функції фільтрую дані згідно певних критеріїв
    def filter_data(self, params, year, region, ticker):
        data = self.getData(params)
        sorted_data = data.loc[(data['Region_Index'] == int(region)) & (data['Year'] == int(year)), [ticker]]
        return sorted_data

    # Збираю усі дані для графіку
    def plot_data(self, filtered_data, region, year, ticker, months_interval):
        start_month, end_month = map(int, months_interval.split('-'))
        plt_object = filtered_data.plot()
        plt_object.set(
            ylabel="Значення",
            xlabel="Тиждень",
            title=f"Графік для області {region}, {year} рік, ряд {ticker}, місяці {start_month}-{end_month}"
        )
        figure = plt_object.get_figure()
        return figure

    # Функція для побудови графіку
    def getPlot(self, params):
        year = int(params['year'])
        region = int(params['region'])
        ticker = params['ticker']
        months_interval = params['months_interval']

        filtered_data = self.filter_data(params, year, region, ticker)
        plot = self.plot_data(filtered_data, region, year, ticker, months_interval)
        return plot


app = SimpleApp()
app.launch(port=5000)
