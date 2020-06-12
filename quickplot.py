'''
Plots the spectrogram of an audio file given its path
'''

from spectrogram import *
from read_wave import *
import matplotlib.pyplot as plt

path = 'train/Claps/MODE AUDIO (50).wav'

signal, sr = read_wave(path)
spec = get_spectrogram(signal, sr)

fig, ax = plt.subplots(nrows=1, ncols=1)

pos = ax.imshow(spec, cmap='winter', interpolation='nearest', aspect='auto')
fig.colorbar(pos, ax=ax)
plt.show()
