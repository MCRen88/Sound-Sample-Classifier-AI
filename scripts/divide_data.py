import os
import shutil
import random

MAIN_DIR = 'good files'
TEST_DIR = 'test'
TRAIN_DIR = 'train'
VAL_DIR = 'validation'

TRAIN_SIZE = 100
TEST_SIZE = 100

TRAIN_SIZE_CRASH = 60
TEST_SIZE_CRASH = 60

classes =  os.listdir(MAIN_DIR)

for c in classes:
    folder = MAIN_DIR + '/' + c
    files = os.listdir(folder)
    random.shuffle(files)

    if (c == 'Crashes'):
        train_files = files[:TRAIN_SIZE_CRASH]
        test_files = files[TRAIN_SIZE_CRASH:TRAIN_SIZE_CRASH+TEST_SIZE_CRASH]
        val_files = files[TRAIN_SIZE_CRASH+TEST_SIZE_CRASH:]
    else:
        train_files = files[:TRAIN_SIZE]
        test_files = files[TRAIN_SIZE:TRAIN_SIZE+TEST_SIZE]
        val_files = files[TRAIN_SIZE+TEST_SIZE:]

    for f in train_files:
        shutil.move(MAIN_DIR + '/' + c + '/' + f, TRAIN_DIR + '/' + c + '/' + f)

    for f in test_files:
        shutil.move(MAIN_DIR + '/' + c + '/' + f, TEST_DIR + '/' + c + '/' + f)

    for f in val_files:
        shutil.move(MAIN_DIR + '/' + c + '/' + f, VAL_DIR + '/' + c + '/' + f)
