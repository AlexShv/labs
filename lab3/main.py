from spyre import server
import pandas as pd


class App(server.App):
    title = 'NOAA data visualization'

    regions_df = pd.read_csv('regions.csv')
    regions_list = regions_df['Region_Name'].tolist()

    inputs = [
        # Список для вибору типу даних NOAA
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
        # Поле вводу початкового тижня
        {
            "type": 'text',
            "label": 'Start Week',
            "key": 'start_week',
            "value": '1',
            "action_id": "update_data"
        },
        # Для кінцевого тижня
        {
            "type": 'text',
            "label": 'End Week',
            "key": 'end_week',
            "value": '52',
            "action_id": "update_data"
        },
        # Поле для року початку
        {
            "type": "text",
            "label": "Year",
            "value": "1982",
            "key": "start_year",
            "action_id": "update_data",
        },
        # Для кінцевого року
        {
            "type": "text",
            "label": "Year",
            "value": "1982",
            "key": "end_year",
            "action_id": "update_data",
        },
    ]

    controls = [{"type": "hidden", "id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [
        {
            "type": "plot",
            "id": "plot_id",
            "control_id": "update_data",
            "tab": "Plot",
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        },
    ]

    # Зчитую дані із файлу
    def getData(self, params):
        data = pd.read_csv('data.csv')
        data = data.dropna(subset=['Year'])
        return data

    # Функція для побудови графіків за вказаними даними
    def getPlot(self, params):

        region = int(params['region'])
        start_week = int(params['start_week'])
        end_week = int(params['end_week'])
        start_year = int(params['start_year'])
        end_year = int(params['end_year'])
        ticker = params['ticker']

        df = self.getData(params)
        df['Year'] = df['Year'].astype(int)

        if end_year == start_year:
            data = df[(df['Region_Index'] == region) & (
                df['Year'] == start_year) & df['Week'].between(start_week, end_week)]
        elif end_year - start_year > 1:
            data = df[(df['Region_Index'] == region)]
            data = data[((data['Year'] == start_year) & (data['Week'] >= start_week)) |
                        ((data['Year'] == end_year) & (data['Week'] <= end_week)) |
                        ((data['Year'] > start_year) & (data['Year'] < end_year))]
        else:
            data = df[(df['Region_Index'] == region)]
            data = data[((data['Year'] == start_year) & (data['Week'] >= start_week)) |
                        ((data['Year'] == end_year) & (data['Week'] <= end_week))]
        data['Date'] = pd.to_datetime(data.Year.astype(str), format='%Y') + \
            pd.to_timedelta(data.Week.mul(7).astype(str) + ' days')

        obj = data.plot(x='Date', y=ticker)
        obj.set_ylabel("NOAA data")
        obj.set_xlabel("Week/Year")
        obj.set_title(f"Plot for region №{region}")

        plot = obj.get_figure()
        return plot

    # Функція для відображення таблиці з даними за певний рік
    def getTable(self, params):

        region = int(params['region'])
        start_year = int(params['start_year'])
        end_year = int(params['end_year'])
        start_week = int(params['start_week'])
        end_week = int(params['end_week'])

        df = self.getData(params)

        if end_week < start_week and start_year >= end_year:
            return pd.DataFrame({'Error': ['Неправильні дані для Start\\End week']})

        if end_week > 52 or start_week > 52:
            return pd.DataFrame({'Error': ['Значення для Start\\End week повинні бути <= 52']})

        data = df[df['Region_Index'] == region]
        data = data[
            ((data['Year'] == start_year) & (data['Week'] >= start_week) & (data['Year'] < end_year)) |
            ((data['Year'] == end_year) & (data['Week'] <= end_week) & (data['Year'] > start_year)) |
            ((data['Year'] == start_year) & (data['Year'] == end_year) & (data['Week'].between(start_week, end_week)))
            ]

        columns = ['Year', 'Week', params['ticker'], 'Region_Index']
        data = data.loc[:, columns].copy()

        return data


app = App()
app.launch()
