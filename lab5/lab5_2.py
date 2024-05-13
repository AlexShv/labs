import numpy as np
import plotly.graph_objs as go
from dash import dcc, html, Input, Output, Dash
from scipy.signal import butter, filtfilt

# Початкові параметри
default_amplitude = 1.0
default_frequency = 1.0
default_phase = 0.0
default_noise_mean = 0.0
default_noise_amplitude = 0.1

time_values = np.arange(0.0, 1.0, 0.001)
noisy_values = np.random.normal(default_noise_mean, default_noise_amplitude, len(time_values))


# Розрахунок гармоніки за формулою
def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_amplitude, show_noise):
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    noisy_signal = signal + noise_amplitude * np.random.normal(noise_mean, 1, len(t)) if show_noise else signal
    return noisy_signal


# Створення інтерфейсу за допомогою Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Harmonic Signal Visualization with Filtering"),
    html.Div([
        html.Label('Visualization Type'),
        dcc.Dropdown(
            id='visualization-type-dropdown',
            options=[
                {'label': 'Original and Filtered Signals', 'value': 'original-and-filtered'},
                {'label': 'Original Signal Only', 'value': 'original-only'},
                {'label': 'Filtered Signal Only', 'value': 'filtered-only'}
            ],
            value='original-and-filtered'
        )
    ]),
    dcc.Graph(id='main-graph'),
    html.Div([
        html.Label('Amplitude'),
        dcc.Slider(id='amplitude-slider', min=0.1, max=10.0, step=0.1, value=default_amplitude),
        html.Label('Frequency'),
        dcc.Slider(id='frequency-slider', min=0.1, max=10.0, step=0.1, value=default_frequency),
        html.Label('Phase'),
        dcc.Slider(id='phase-slider', min=0.0, max=2*np.pi, step=0.1, value=default_phase),
        html.Label('Noise Mean'),
        dcc.Slider(id='noise-mean-slider', min=-1.0, max=1.0, step=0.1, value=default_noise_mean),
        html.Label('Noise Amplitude'),
        dcc.Slider(id='noise-amplitude-slider', min=0.0, max=1.0, step=0.1, value=default_noise_amplitude),
        html.Label('Cutoff Frequency'),
        dcc.Slider(id='cutoff-frequency-slider', min=0.1, max=10.0, step=0.1, value=1.0),
        html.Label('Show Noise'),
        dcc.Checklist(id='show-noise-checkbox', options=[{'label': 'Show Noise', 'value': 'show'}], value=['show']),
        html.Button('Reset', id='reset-button')
    ], style={'width': '50%', 'margin': 'auto', 'textAlign': 'center'})
])


@app.callback(
    Output('main-graph', 'figure'),
    [
        Input('visualization-type-dropdown', 'value'),
        Input('amplitude-slider', 'value'),
        Input('frequency-slider', 'value'),
        Input('phase-slider', 'value'),
        Input('noise-mean-slider', 'value'),
        Input('noise-amplitude-slider', 'value'),
        Input('cutoff-frequency-slider', 'value'),
        Input('show-noise-checkbox', 'value'),
        Input('reset-button', 'n_clicks')
    ]
)
def update_graph(visualization_type, amplitude, frequency, phase, noise_mean, noise_amplitude, cutoff_frequency, show_noise, n_clicks):
    if n_clicks is not None and n_clicks > 0:
        amplitude = default_amplitude
        frequency = default_frequency
        phase = default_phase
        noise_mean = default_noise_mean
        noise_amplitude = default_noise_amplitude

    y = harmonic_with_noise(time_values, amplitude, frequency, phase, noise_mean, noise_amplitude, 'show' in show_noise)

    # Фільтруємо сигнал
    nyquist = 0.5 * 1000
    normal_cutoff = cutoff_frequency / nyquist
    b, a = butter(5, normal_cutoff, btype='low', analog=False)
    filtered_signal = filtfilt(b, a, y)

    fig = go.Figure()

    if visualization_type == 'original-and-filtered' or visualization_type == 'original-only':
        fig.add_trace(go.Scatter(x=time_values, y=y, mode='lines', name='Original Signal'))
    if visualization_type == 'original-and-filtered' or visualization_type == 'filtered-only':
        fig.add_trace(go.Scatter(x=time_values, y=filtered_signal, mode='lines', name='Filtered Signal'))

    fig.update_layout(title="Harmonic Signal with Filtering",
                      xaxis_title="Time",
                      yaxis_title="Amplitude")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
