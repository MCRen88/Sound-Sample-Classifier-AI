'''
Script that performs signal preprocessing on audio files so that they are ready to be used by the model
Processed data for each test set is written to the appropriate .csv file
'''

import os
import numpy as np
from tqdm import tqdm
import read_wave as rw
import spectrogram as sp

# Stored wave file locations
TRAIN_DIR = 'train'
TEST_DIR = 'test'
VALIDATION_DIR = 'validation'

# Feaeture outputs
TRAIN_OUT = 'train_data.csv'
TEST_OUT = 'test_data.csv'
VALIDATION_OUT = 'validation_data.csv'

CLASSES = ['Claps',
            'Crashes',
            'HiHats',
            'Kicks',
            'Snares']

directories = [TRAIN_DIR, TEST_DIR, VALIDATION_DIR]
out_files = [TRAIN_OUT, TEST_OUT, VALIDATION_OUT]

# spectrogram parameters
frame_length=0.025
frame_offset=0.01
lowFreq=300
hiFreq=10000
numFilters=26
numFrames=75

numDataPoints = numFilters * numFrames

for dir, out in zip(directories, out_files):
    print("Writing " + dir + " data to: " + out)
    # Get filepaths of samples for each class
    class_files = {}
    for c in CLASSES:
        files = os.listdir(dir + '/' + c)
        class_files[c] = files

    # Read, process, and write data of each sample to a csv file
    data = []
    for c in class_files:
        print("Class being processed: " + c)
        files = class_files[c]
        paths = []
        for file in files:
            paths.append(dir + '/' + c + '/' + file)

        for path in tqdm(paths):
            signal, sr = rw.read_wave(path, normalize=True, length=1, threshold=0.001)
            spec = sp.get_spectrogram(signal, sr, frame_length=frame_length, frame_offset=frame_offset, lowFreq=lowFreq, hiFreq=hiFreq, numFilters=numFilters, numFrames=numFrames)
            dataToWrite = np.append(np.array([c]), spec.flatten())
            data.append(dataToWrite)

    header = ['Class']
    header.extend(['D' + str(i) for i in range(numDataPoints)])
    df = pd.DataFrame(columns=header, data=data)
    df.to_csv(out)
