import numpy as np
import matplotlib.pyplot as plt


def generate_impulse_response(cutoff_freq, fs, num_taps=101):
    nyquist_freq = fs / 2.0
    cutoff_normal = cutoff_freq / nyquist_freq
    h = np.zeros(num_taps)
    for i in range(num_taps):
        if i - num_taps // 2 == 0:
            h[i] = 2 * np.pi * cutoff_normal
        else:
            h[i] = np.sin(2 * np.pi * cutoff_normal * (i - num_taps // 2)) / (i - num_taps // 2)
    h = h * np.hamming(num_taps)
    return h / np.sum(h)


def simple_lowpass_filter(data, cutoff_freq, fs):
    h = generate_impulse_response(cutoff_freq, fs)

    num_taps = len(h)
    N = len(data)
    filtered_data = np.zeros_like(data)
    for n in range(N):
        for k in range(num_taps):
            if n - k >= 0:
                filtered_data[n] += data[n - k] * h[k]
    return filtered_data


fs = 1000.0
t = np.arange(0, 1, 1 / fs)
frequency = 10
signal = np.sin(2 * np.pi * frequency * t)
cutoff_freq = 30

filtered_signal = simple_lowpass_filter(signal, cutoff_freq, fs)

plt.figure(figsize=(10, 6))
plt.plot(t, signal, label='Вхідний сигнал')
plt.plot(t, filtered_signal, label='Відфільтрований сигнал')
plt.xlabel('Час (с)')
plt.ylabel('Амплітуда')
plt.title('Вхідний та відфільтрований сигнали')
plt.legend()
plt.grid(True)
plt.show()
