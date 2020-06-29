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

# Datasetes
TRAIN_SET = 'train_data.csv'
TEST_SET = 'test_data.csv'

# Labels
CLASSES = ['Crashes',
            'HiHats',
            'Kicks',
            'Snares']

numFilters=26
numFrames=75
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
train_features = train_df.reshape((len(train_df), numFilters, numFrames))
train_features = np.expand_dims(train_features, 3) # Gives data shape of (numFilters, numFrames, 1) for Conv2D net

test_labels = test_labels.to_numpy(dtype='uint8')
test_df = test_df.to_numpy()
test_features = test_df.reshape((len(test_df), numFilters, numFrames))
test_features = np.expand_dims(test_features, 3)

# Display data information
print("Training data has shape: " + str(np.shape(train_features[0])))
print("Testing data has shape: " + str(np.shape(test_features[0])))
print("# training data points: " + str(len(train_features)))
print("# testing data points: " + str(len(test_features)))

# Create and fit model
while True:
    model = model_module.createModel()
    model.summary()
    print("Press any key to continue...")
    input()
    model.fit(train_features, train_labels, epochs=50)

    # Evaluate
    test_loss, test_acc = model.evaluate(test_features,  test_labels, verbose=2)
    print('Test accuracy:', test_acc)

    # Save
    print("Save current model? (y/n)")
    response = input()
    if response == 'y':
        model.save("saved_models/" + MODEL + ".h5")
        print("Model saved")

    print("Reset and retrain weights of this model? (y/n)")
    response = input()
    if response == 'n':
        break
