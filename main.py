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

CLASSES = ['Claps',
            'Crashes',
            'HiHats',
            'Kicks',
            'Snares']

# spectrogram parameters
frame_length=0.025
frame_offset=0.01
lowFreq=300
hiFreq=10000
numFilters=26
numFrames=75

def importModel(model_name):
    m = importlib.import_module(model_name)
    model = m.createModel()
    ckpt = 'model_checkpoints/' + model_name + '/' + model_name
    model.load_weights(ckpt)
    return model

def makePrediction(model, path):
    signal, sr = rw.read_wave(path, normalize=True, length=1, threshold=0.001)
    spec = sp.get_spectrogram(signal, sr, frame_length=frame_length, frame_offset=frame_offset, lowFreq=lowFreq, hiFreq=hiFreq, numFilters=numFilters, numFrames=numFrames)
    features = spec.flatten()

    modelInput = np.array([features])

    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    prob = probability_model.predict(modelInput)

    predictedClass = np.argmax(prob[0])
    return predictedClass

def main():
    parser = argparse.ArgumentParser(description="Run Model Prediction on a Audio Sample")
    parser.add_argument("modelName", help="Indicate model filename (exclude .py extension)")
    parser.add_argument("filepath", help="Indicate path to audio file (must be .wav file)")

    args = parser.parse_args()
    modelName = args.modelName
    filepath = args.filepath

    model = importModel(modelName)
    prediction = makePrediction(model, filepath)
    print("\n\nPredicted sample type for: " + filepath + " is: " + CLASSES[prediction])

if __name__ == '__main__':
    main()
