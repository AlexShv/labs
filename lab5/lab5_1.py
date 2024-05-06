import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
import numpy as np

# Початкові параметри
default_amplitude = 1.0
default_frequency = 1.0
default_phase = 0.0
default_noise_mean = 0.0
default_noise_amplitude = 0.1

time_values = np.arange(0.0, 1.0, 0.001)
noisy_values = np.random.normal(default_noise_mean, default_noise_amplitude, len(time_values))

# Збереження попередніх значень для порівняння
prev_amplitude = default_amplitude
prev_frequency = default_frequency
prev_phase = default_phase
prev_noise_mean = default_noise_mean
previous_noise_amplitude = default_noise_amplitude


# Розрахунок гармоніки за формулою
def harmonic_with_noise(t, amplitude, frequency, phase, show_noise):
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    noisy_signal = signal + noisy_values if show_noise else signal
    return noisy_signal


# Створення основного вікна
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.4)

s = harmonic_with_noise(
    time_values, default_amplitude, default_frequency, default_phase, True
)
l, = plt.plot(time_values, s, lw=2)


instructions = '''
Інструкції щодо користуванням програмою:
- Змінюйте значення слайдерів, щоб налаштувати амплітуду, частоту та фазовий зсув гармоніки,
  а також амплітуду шуму
- Прапорець "Show Noise" включає або вимикає відображення шуму на графіку
- Щоб скинути параметри до початкових значень, натисніть кнопку "Reset"
'''

plt.figtext(0.5, 1.02, instructions, ha='center', va='top')
plt.xlabel('Time')
plt.ylabel('Amplitude')

# Визначення положення слайдерів та створення їх
ax_amplitude = plt.axes((0.1, 0.25, 0.65, 0.03))
ax_frequency = plt.axes((0.1, 0.2, 0.65, 0.03))
ax_phase = plt.axes((0.1, 0.15, 0.65, 0.03))
ax_noise_mean = plt.axes((0.1, 0.1, 0.65, 0.03))
ax_noise_amplitude = plt.axes((0.1, 0.05, 0.65, 0.03))

amplitude_slider = Slider(ax_amplitude, 'Amplitude', 0.1, 10.0, valinit=default_amplitude)
frequency_slider = Slider(ax_frequency, 'Frequency', 0.1, 10.0, valinit=default_frequency)
phase_slider = Slider(ax_phase, 'Phase', 0.0, 2 * np.pi, valinit=default_phase)
noise_mean_slider = Slider(ax_noise_mean, 'Noise Mean', -1.0, 1.0, valinit=default_noise_mean)
noise_amplitude_slider = Slider(ax_noise_amplitude, 'Noise Amplitude', 0.0, 1.0, valinit=default_noise_amplitude)


# Функція оновлення графіку
def update(val):
    global prev_amplitude, prev_frequency, prev_phase, prev_noise_mean, previous_noise_amplitude

    amplitude = amplitude_slider.val
    frequency = frequency_slider.val
    phase = phase_slider.val
    noise_mean = noise_mean_slider.val
    noise_amplitude = noise_amplitude_slider.val

    show_noise = check_show_noise.get_status()[0]

    # Перевірка зміни параметрів гармоніки
    if (amplitude != prev_amplitude) or (frequency != prev_frequency) or (phase != prev_phase):
        y = harmonic_with_noise(time_values, amplitude, frequency, phase, show_noise)
        l.set_ydata(y)
        prev_amplitude = amplitude
        prev_frequency = frequency
        prev_phase = phase

    # Перевірка зміни параметрів шуму
    if (noise_mean != prev_noise_mean) or (noise_amplitude != previous_noise_amplitude):
        global noisy_values
        noisy_values = np.random.normal(noise_mean, noise_amplitude, len(time_values))
        y = harmonic_with_noise(time_values, amplitude, frequency, phase, show_noise)
        l.set_ydata(y)
        prev_noise_mean = noise_mean
        previous_noise_amplitude = noise_amplitude

    fig.canvas.draw_idle()
    ax.set_ylim(-amplitude * 1.5, amplitude * 1.5)


amplitude_slider.on_changed(update)
frequency_slider.on_changed(update)
phase_slider.on_changed(update)
noise_mean_slider.on_changed(update)
noise_amplitude_slider.on_changed(update)


# Функція для кнопки "Reset"
def reset(event):
    amplitude_slider.reset()
    frequency_slider.reset()
    phase_slider.reset()
    noise_mean_slider.reset()
    noise_amplitude_slider.reset()


ax_reset = plt.axes((0.8, 0.025, 0.1, 0.04))
button_reset = Button(ax_reset, 'Reset')
button_reset.on_clicked(reset)


# Додавання чекбоксу
rax = plt.axes((0.9, 0.45, 0.1, 0.15), facecolor='yellow')
check_show_noise = CheckButtons(rax, ['Show Noise'], [True])
check_show_noise.on_clicked(update)

plt.show()
