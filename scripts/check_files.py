import os
from read_wave import *
from tqdm import tqdm

DIR_TO_CHECK = 'files to check'

files = os.listdir(DIR_TO_CHECK)

for file in files:
    path = DIR_TO_CHECK + '/' + file
    signal, sr = read_wave(path, normalize=True, length=1, threshold=0.001)
    if signal is None or sr is None:
        print("File" + file + " is not compatible")

print("Files are compatible")
