#####################################
# Module to streamline file access  #
#####################################

from wav_unpacker import *

TEST_DIR = "wav_files"
FILE_1 = "1.wav"
FILE_2 = "2.wav"
FILE_3 = "3.wav"
FILE_4 = "note.wav" # G note (octaves at:
                    # 391.995
                    # 783.991 Hz
                    # 1567.982 Hz or other multiples
FILE_5 = 'A5.wav' #880 Hz

def config_test_file(dir, filename):
    return dir + '/' + filename

test_file_1 = config_test_file(TEST_DIR, FILE_1)
test_file_2 = config_test_file(TEST_DIR, FILE_2)
test_file_3 = config_test_file(TEST_DIR, FILE_3)
test_file_4 = config_test_file(TEST_DIR, FILE_4)
test_file_5 = config_test_file(TEST_DIR, FILE_5)

wav_obj_1 = WaveObject(test_file_1)
wav_obj_2 = WaveObject(test_file_2)
wav_obj_3 = WaveObject(test_file_3)
wav_obj_4 = WaveObject(test_file_4)
wav_obj_5 = WaveObject(test_file_5)

test_group_1 = (wav_obj_1, wav_obj_2, wav_obj_3) # Group of valid wave files for testing

wav_obj_1_normalized = WaveObject(test_file_1, normalize=True, normLevel=1)
wav_obj_2_normalized = WaveObject(test_file_2, normalize=True, normLevel=1)
wav_obj_3_normalized = WaveObject(test_file_3, normalize=True, normLevel=1)
wav_obj_4_normalized = WaveObject(test_file_4, normalize=True, normLevel=1)
wav_obj_5_normalized = WaveObject(test_file_5, normalize=True, normLevel=1)
