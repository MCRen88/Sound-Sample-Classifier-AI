'''

'''
import os
import pandas as pd
import numpy as np
from tqdm import tqdm

import read_wave as rw
import spectrogram as sp

RAW_DIR = 'wav_files'
CLASSES = ['Claps',
            'Crashes',
            'HiHats',
            'Kicks',
            'Snares']

OUT_FILE = 'data.csv'

# spectrogram parameters
frame_length=0.025
frame_offset=0.01
lowFreq=300
hiFreq=10000
numFilters=26
numFrames=75

numDataPoints = numFilters * numFrames

# Get filepaths of samples for each class
class_files = {}
for c in CLASSES:
    files = os.listdir(RAW_DIR + '/' + c)
    class_files[c] = files

# Read, process, and write data of each sample to a csv file
data = []
for c in tqdm(class_files):
    files = class_files[c]
    paths = []
    for file in files:
        paths.append(RAW_DIR + '/' + c + '/' + file)

    for path in paths:
        signal, sr = rw.read_wave(path, normalize=True, length=1, threshold=0.001)
        spec = sp.get_spectrogram(signal, sr, frame_length=frame_length, frame_offset=frame_offset, lowFreq=lowFreq, hiFreq=hiFreq, numFilters=numFilters, numFrames=numFrames)
        dataToWrite = np.append(np.array([c]), spec.flatten())
        data.append(dataToWrite)

header = ['Class']
header.extend(['D' + str(i) for i in range(numDataPoints)])
df = pd.DataFrame(columns=header, data=data)
df.to_csv(OUT_FILE)
