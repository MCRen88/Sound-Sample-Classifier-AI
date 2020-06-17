'''
Basic NN, achieves ~ 80% accuracy on test set
'''

import tensorflow as tf
from tensorflow import keras

import numpy as np
import pandas as pd

def createModel():
    model = keras.Sequential([
        keras.layers.Input(shape=(1950,)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(32, activation='sigmoid'),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(5)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    return model
