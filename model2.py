'''
Convolutional Network
'''

import tensorflow as tf
from tensorflow import keras

import numpy as np
import pandas as pd

numFilters=26
numFrames=75

def createModel():
    model = keras.Sequential([
        keras.layers.Conv2D(filters=16, kernel_size=(3, 3), activation='relu', input_shape=(numFilters, numFrames, 1)),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu'),
        keras.layers.Flatten(),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(4)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    return model
