import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
import numpy as np
from scipy.signal import butter, filtfilt

# Початкові параметри
default_amplitude = 1.0
default_frequency = 1.0
default_phase = 0.0
default_noise_mean = 0.0
default_noise_amplitude = 0.1
initial_cutoff_frequency = 40.0

time_values = np.arange(0.0, 1.0, 0.001)
noisy_values = np.random.normal(default_noise_mean, default_noise_amplitude, len(time_values))

# Збереження старих значень для порівняння
prev_amplitude = default_amplitude
prev_frequency = default_frequency
prev_phase = default_phase
prev_noise_mean = default_noise_mean
prev_noise_amplitude = default_noise_amplitude
prev_cutoff_frequency = initial_cutoff_frequency


# Розрахунок гармоніки за формулою
def harmonic_with_noise(t, amplitude, frequency, phase, show_noise):
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    noisy_signal = signal + noisy_values if show_noise else signal
    return noisy_signal


# Фільтрування сигналу
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y


# Створення основного вікна
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.5)

s = harmonic_with_noise(
    time_values, default_amplitude, default_frequency, default_phase, True
)
l, = plt.plot(time_values, s, lw=2, label='Noisy Harmonic Signal')

# Відфільтрована гармоніка
filtered_signal = butter_lowpass_filter(s, initial_cutoff_frequency, 1000)
l_filtered, = plt.plot(time_values, filtered_signal, lw=2, ls='--', label='Filtered Signal')

instructions = '''
Інструкції щодо користуванням програмою:
- Змінюйте значення слайдерів, щоб налаштувати амплітуду, частоту та фазовий зсув гармоніки,
  а також амплітуду шуму та частоту відсічення фільтру
- Прапорець "Show Noise" включає або вимикає відображення шуму на графіку
- Щоб скинути параметри до початкових значень, натисніть кнопку "Reset"
'''

plt.figtext(0.5, 1.02, instructions, ha='center', va='top')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

# Визначаю положення слайдерів та створюю їх
ax_amplitude = plt.axes((0.1, 0.35, 0.65, 0.03))
ax_frequency = plt.axes((0.1, 0.3, 0.65, 0.03))
ax_phase = plt.axes((0.1, 0.25, 0.65, 0.03))
ax_noise_mean = plt.axes((0.1, 0.2, 0.65, 0.03))
ax_noise_amplitude = plt.axes((0.1, 0.15, 0.65, 0.03))
ax_cutoff = plt.axes((0.1, 0.1, 0.65, 0.03))

s_amplitude = Slider(ax_amplitude, 'Amplitude', 0.1, 10.0, valinit=default_amplitude)
s_frequency = Slider(ax_frequency, 'Frequency', 0.1, 10.0, valinit=default_frequency)
s_phase = Slider(ax_phase, 'Phase', 0.0, 2 * np.pi, valinit=default_phase)
s_noise_mean = Slider(ax_noise_mean, 'Noise Mean', -1.0, 1.0, valinit=default_noise_mean)
s_noise_amplitude = Slider(ax_noise_amplitude, 'Noise Amplitude', 0.0, 1.0, valinit=default_noise_amplitude)
s_cutoff = Slider(ax_cutoff, 'Cutoff Frequency', 1.0, 100.0, valinit=initial_cutoff_frequency)


# Функція оновлення графіку
def update(val):
    global prev_amplitude, prev_frequency, prev_phase, prev_noise_mean, prev_noise_amplitude, prev_cutoff_frequency, filtered_signal

    amplitude = s_amplitude.val
    frequency = s_frequency.val
    phase = s_phase.val
    noise_mean = s_noise_mean.val
    noise_amplitude = s_noise_amplitude.val
    cutoff = s_cutoff.val

    show_noise = check_show_noise.get_status()[0]

    # Перевірка зміни параметрів гармоніки
    if (amplitude != prev_amplitude) or (frequency != prev_frequency) or (phase != prev_phase):
        y = harmonic_with_noise(time_values, amplitude, frequency, phase, show_noise)
        l.set_ydata(y)
        prev_amplitude = amplitude
        prev_frequency = frequency
        prev_phase = phase

    # Фільтрування сигналу
    if (amplitude != prev_amplitude) or (frequency != prev_frequency) or \
            (phase != prev_phase) or (noise_mean != prev_noise_mean) or \
            (noise_amplitude != prev_noise_amplitude) or (cutoff != prev_cutoff_frequency):
        if 'filtered_signal' not in globals():
            filtered_signal = np.zeros_like(y)
        filtered_signal = butter_lowpass_filter(filtered_signal, cutoff, 1000)
        l_filtered.set_ydata(filtered_signal)

    # Перевірка зміни параметрів шуму
    if (noise_mean != prev_noise_mean) or (noise_amplitude != prev_noise_amplitude):
        global noisy_values
        noisy_values = np.random.normal(noise_mean, noise_amplitude, len(time_values))
        y = harmonic_with_noise(time_values, amplitude, frequency, phase, show_noise)
        l.set_ydata(y)
        prev_noise_mean = noise_mean
        prev_noise_amplitude = noise_amplitude

    fig.canvas.draw_idle()
    ax.set_ylim(-amplitude * 1.5, amplitude * 1.5)


s_amplitude.on_changed(update)
s_frequency.on_changed(update)
s_phase.on_changed(update)
s_noise_mean.on_changed(update)
s_noise_amplitude.on_changed(update)
s_cutoff.on_changed(update)


# Функція для кнопки "Reset"
def reset(event):
    s_amplitude.reset()
    s_frequency.reset()
    s_phase.reset()
    s_noise_mean.reset()
    s_noise_amplitude.reset()
    s_cutoff.reset()


ax_reset = plt.axes((0.8, 0.025, 0.1, 0.04))
button_reset = Button(ax_reset, 'Reset')
button_reset.on_clicked(reset)

# Додавання чекбоксу
rax = plt.axes((0.9, 0.45, 0.1, 0.15), facecolor='yellow')
check_show_noise = CheckButtons(rax, ['Show Noise'], [True])
check_show_noise.on_clicked(update)

plt.show()
