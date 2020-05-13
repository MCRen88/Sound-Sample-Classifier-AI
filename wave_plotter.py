############################################################
# Module to handle wave file data plotting  #
############################################################
from scipy.fftpack import fft
import math
import matplotlib.pyplot as plt
from file_manage import *


def plot_time_domain(wav_obj):
    left_data = wav_obj.data.frames[0]
    right_data = wav_obj.data.frames[1]
    avg_data = [(l + r) / 2 for l, r in zip(left_data, right_data)]

    plt.figure(1)
    plt.plot(avg_data)
    plt.title("Average Data Frame Values")
    plt.xlabel('Frame #')


    plt.figure(2)
    plt.subplot(211)
    plt.title("Channel Seperated Data Frame Values")
    plt.plot(left_data)
    plt.ylabel("Left")
    plt.subplot(212)
    plt.plot(right_data)
    plt.ylabel("Right")
    plt.xlabel('Frame #')

    plt.show()

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

    freq_x = [val/T for val in k]

    plt.figure(1)
    plt.plot(freq_x, fft_to_plot)
    plt.show()

if __name__ == "__main__":
    plot_freq_domain(wav_obj_4)
