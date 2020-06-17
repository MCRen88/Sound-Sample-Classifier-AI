'''
Read spectrogram information from a .csv file and print it accordingly
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

numFilters = 26
numFrames = 75

df = pd.read_csv('validation_data.csv')
data = df.loc[0]

arr = data.to_numpy()[2:]

spec = np.resize(arr, (numFilters, numFrames))
spec = spec.tolist()

fig, ax = plt.subplots(nrows=1, ncols=1)
pos = ax.imshow(spec, cmap='winter', interpolation='nearest', aspect='auto')
fig.colorbar(pos, ax=ax)
plt.show()
