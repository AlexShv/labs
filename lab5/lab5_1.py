import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt
import numpy as np

# Початкові параметри
default_amplitude = 1.0
default_frequency = 1.0
default_phase = 0.0
default_noise_mean = 0.0
default_noise_amplitude = 0.1

time_values = np.arange(0.0, 1.0, 0.001)
noisy_values = np.random.normal(default_noise_mean, default_noise_amplitude, len(time_values))

# Збереження попередніх значень для порівнянням
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


def butterworth_filter(signal, cutoff_frequency, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff_frequency / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal


# Створення основного вікна
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.4)

s = harmonic_with_noise(
    time_values, default_amplitude, default_frequency, default_phase, True
)
l, = plt.plot(time_values, s, lw=2)
l_filt, = plt.plot(time_values, s, lw=2)  # Ініціалізація графіка для відфільтрованої гармоніки

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
def update(val=None):
    global prev_noise_mean, previous_noise_amplitude
    amplitude = amplitude_slider.val
    frequency = frequency_slider.val
    phase = phase_slider.val
    noise_mean = noise_mean_slider.val
    noise_amplitude = noise_amplitude_slider.val

    show_noise = check_show_noise.get_status()[0]

    # Оновлюємо noisy_values з урахуванням нових параметрів шуму, якщо вони змінилися
    if noise_mean != prev_noise_mean or noise_amplitude != previous_noise_amplitude:
        global noisy_values
        noisy_values = np.random.normal(noise_mean, noise_amplitude, len(time_values))

    # Оновлюємо графік з урахуванням стану чекбокса
    y = harmonic_with_noise(time_values, amplitude, frequency, phase, show_noise)
    l.set_ydata(y)

    # Фільтруємо сигнал
    cutoff_frequency = cutoff_frequency_slider.val
    fs = 1000  # Частота дискретизації
    filtered_signal = butterworth_filter(y, cutoff_frequency, fs)
    l_filt.set_ydata(filtered_signal)

    fig.canvas.draw_idle()
    ax.set_ylim(-amplitude * 1.5, amplitude * 1.5)

    # Переміщуємо глобальну декларацію після використання змінних
    prev_noise_mean = noise_mean
    previous_noise_amplitude = noise_amplitude


# Функція для кнопки "Reset"
def reset(event):
    amplitude_slider.reset()
    frequency_slider.reset()
    phase_slider.reset()
    noise_mean_slider.reset()
    noise_amplitude_slider.reset()


# Функція для оновлення графіку при зміні стану чекбоксу
def update_show_noise(label):
    update()


# Пов'язання функції з обробником подій чекбоксу
rax = plt.axes((0.9, 0.45, 0.1, 0.15), facecolor='yellow')
check_show_noise = CheckButtons(rax, ['Show Noise'], [True])
check_show_noise.on_clicked(update_show_noise)

amplitude_slider.on_changed(update)
frequency_slider.on_changed(update)
phase_slider.on_changed(update)
noise_mean_slider.on_changed(update)
noise_amplitude_slider.on_changed(update)

ax_reset = plt.axes((0.8, 0.025, 0.1, 0.04))
button_reset = Button(ax_reset, 'Reset')
button_reset.on_clicked(reset)

# Створення слайдера для вибору частоти відсічки фільтра Баттерворта
ax_cutoff_frequency = plt.axes((0.1, 0.3, 0.65, 0.03))
cutoff_frequency_slider = Slider(ax_cutoff_frequency, 'Cutoff Frequency', 0.1, 10.0, valinit=1.0)
cutoff_frequency_slider.on_changed(update)

ax.grid(True)

plt.legend()
plt.show()
