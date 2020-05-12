############################################################
# Module to handle wave file data plotting  #
############################################################

import matplotlib.pyplot as plt
from file_manage import *


def plot_waveform(wav_obj):
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

if __name__ == "__main__":
    plot_waveform(wav_obj_3_normalized)
