'''
Basic NN, achieves ~ 80% accuracy on test set
'''

import tensorflow as tf
from tensorflow import keras

import numpy as np
import pandas as pd

numFilters=26
numFrames=75

def createModel():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(numFilters, numFrames, 1)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(4)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    return model
