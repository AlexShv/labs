import numpy as np
import plotly.graph_objs as go
from dash import dcc, html, Input, Output, Dash

# Початкові параметри
default_amplitude = 1.0
default_frequency = 1.0
default_phase = 0.0
default_noise_mean = 0.0
default_noise_amplitude = 0.1
default_show_noise = True

time_values = np.arange(0.0, 1.0, 0.001)
noisy_values = np.random.normal(default_noise_mean, default_noise_amplitude, len(time_values))


# Розрахунок гармоніки за формулою
def harmonic_with_noise(t, amplitude, frequency, phase, show_noise):
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    noisy_signal = signal + noisy_values if show_noise else signal
    return noisy_signal


app = Dash(__name__)

# Опис інтерфейсу
app.layout = html.Div([
    html.H1("Графік гармоніки з шумом"),
    dcc.Graph(id='harmonic-graph'),
    html.Label("Амплітуда:"),
    dcc.Slider(id='amplitude-slider', min=0.1, max=10.0, step=0.1, value=default_amplitude),
    html.Label("Частота:"),
    dcc.Slider(id='frequency-slider', min=0.1, max=10.0, step=0.1, value=default_frequency),
    html.Label("Фазовий зсув:"),
    dcc.Slider(id='phase-slider', min=0.0, max=2 * np.pi, step=0.1, value=default_phase),
    html.Label("Показати шум:"),
    dcc.Checklist(id='show-noise', options=[{'label': 'Так', 'value': True}], value=[True]),
    html.Button('Скинути', id='reset-button'),
])


# Функція для оновлення графіку
@app.callback(
    Output('harmonic-graph', 'figure'),
    [Input('amplitude-slider', 'value'),
     Input('frequency-slider', 'value'),
     Input('phase-slider', 'value'),
     Input('show-noise', 'value'),
     Input('reset-button', 'n_clicks')]
)
def update_graph(amplitude, frequency, phase, show_noise, n_clicks):
    if n_clicks:
        amplitude = default_amplitude
        frequency = default_frequency
        phase = default_phase
        show_noise = default_show_noise

    y_values = harmonic_with_noise(time_values, amplitude, frequency, phase, show_noise)
    trace = go.Scatter(x=time_values, y=y_values, mode='lines', name='Гармоніка з шумом')
    layout = go.Layout(title='Графік гармоніки з шумом', xaxis=dict(title='Час'), yaxis=dict(title='Амплітуда'))
    return {'data': [trace], 'layout': layout}


if __name__ == '__main__':
    app.run_server(debug=True)