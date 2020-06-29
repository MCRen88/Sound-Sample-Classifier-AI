'''
Command line interface to make predictions using a saved keras model
'''

import tensorflow as tf
from tensorflow import keras

import numpy as np
import pandas as pd

import argparse
import importlib
import read_wave as rw
import spectrogram as sp

import logging
import os

# Supress tf printouts
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.FATAL)

CLASSES = ['Crash',
            'HiHat',
            'Kick',
            'Snare']

# spectrogram parameters
frame_length=0.025
frame_offset=0.01
lowFreq=300
hiFreq=10000
numFilters=26
numFrames=75

def importModel():
    print("Enter Model Path (exclude .h5 extention)")
    model_name = input()
    m = importlib.import_module(model_name)
    model = keras.models.load_model("saved_models/" + model_name + '.h5')
    return model

def makePrediction(model, sample):
    if model is None:
        print("Load a model!")
        return

    if sample is None:
        print("Load a sample!")
        return

    print("Predicting...")
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    prob = probability_model.predict(sample)
    predictedClass = CLASSES[np.argmax(prob[0])]
    print("Predicted class of audio sample: " + predictedClass)

def loadSample():
    print("Enter full path to .wav file")
    path = input()
    signal, sr = rw.read_wave(path, normalize=True, length=1, threshold=0.001)
    spec = sp.get_spectrogram(signal, sr, frame_length=frame_length, frame_offset=frame_offset, lowFreq=lowFreq, hiFreq=hiFreq, numFilters=numFilters, numFrames=numFrames)
    return np.array([spec])

def main():
    clear = 'cls' if os.name == 'nt' else 'clear'
    print("Welcome to sound sample predictor!")

    model = None
    sample = None

    while True:
        print("1. Load Model")
        print("2. Load Sample")
        print("3. Predict using Model")
        print("4. Summarize Model")
        print("5. Exit")

        val = input()
        os.system(clear)

        if val not in '12345':
            print("Select a valid command!")

        elif val == '1':
            model = importModel()

        elif val == '2':
            sample = loadSample()

        elif val == '3':
            makePrediction(model, sample)

        elif val == '4':
            if model is None:
                print("Load a Model!")
            else:
                model.summary()

        elif val == '5':
            print("Exiting now...")
            break


if __name__ == '__main__':
    main()
