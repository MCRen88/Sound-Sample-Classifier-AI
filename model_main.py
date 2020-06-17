'''
Imports model architecture, trains, and saves checkpoint
'''

import tensorflow as tf
from tensorflow import keras

import numpy as np
import pandas as pd
import importlib
import os

# Model to be used
MODEL = 'model1'
model_module =  importlib.import_module(MODEL)

# Checkpoint to save model
model_save = 'model_checkpoints/' + MODEL + '/' + MODEL
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=model_save,
                                                 save_weights_only=True,
                                                 verbose=1)

# Datasetes
TRAIN_SET = 'train_data.csv'
TEST_SET = 'test_data.csv'

# Labels
CLASSES = ['Claps',
            'Crashes',
            'HiHats',
            'Kicks',
            'Snares']

# Import data
train_df = pd.read_csv(TRAIN_SET)
test_df =  pd.read_csv(TEST_SET)

train_labels = train_df.pop('Class')
test_labels = test_df.pop('Class')

# Give labels discrete values
for i in range(len(train_labels)):
    train_labels[i] = CLASSES.index(train_labels[i])

for i in range(len(test_labels)):
    test_labels[i] = CLASSES.index(test_labels[i])

train_labels = train_labels.to_numpy(dtype='uint8')
train_df = train_df.to_numpy()

test_labels = test_labels.to_numpy(dtype='uint8')
test_df = test_df.to_numpy()

# Train model
model = model_module.createModel()
model.fit(train_df, train_labels, epochs=50, callbacks=[cp_callback])

# Evaluate
test_loss, test_acc = model.evaluate(test_df,  test_labels, verbose=2)
print('Test accuracy:', test_acc)
