#############################################
# Module to handle wave file data plotting  #
#############################################
from scipy.fftpack import fft
import math
import matplotlib.pyplot as plt
from file_manage import *


def plot_time_domain(wav_obj):
    plt.figure(1)
    plt.plot(wav_obj.data.avg)
    plt.title("Time Domain Analysis")
    plt.xlabel('Frame #')
    plt.ylabel('Amplitude')
    plt.grid(True, 'both', 'both')

    axes = plt.gca()
    axes.set_xlim([0, None])


def plot_freq_domain(wav_obj):
    # First combine stereo tracks into a mono data
    left_data = wav_obj.data.frames[0]
    right_data = wav_obj.data.frames[1]
    avg_data = [(l + r) / 2 for l, r in zip(left_data, right_data)]

    # fft() gives the full fourier transform
    # we only need the first half (real) and its magnitude
    freq_response = fft(avg_data)
    fft_to_plot = [abs(x) for x in freq_response[0:len(freq_response)//2]]

    k = range(len(fft_to_plot))
    T = len(fft_to_plot) / wav_obj.header.sampleRate

    freq_x = [val/(T * 2) for val in k]

    plt.figure(3)
    plt.plot(freq_x, fft_to_plot)
    plt.title("Fast Fourier Transform Analysis")
    plt.ylabel("Amplitude")
    plt.xlabel("Frequency (Hz)")
    plt.grid(True, 'both', 'both')

    axes = plt.gca()
    axes.set_xlim([0, None])
    axes.set_ylim([0, None])

if __name__ == "__main__":
    plot_freq_domain(wav_obj_5_normalized)
    plot_time_domain(wav_obj_5_normalized)

    plt.show()
