#####################################
# Module to streamline file access  #
#####################################

from wav_unpacker import *

TEST_DIR = "wav_files"
FILE_1 = "1.wav"
FILE_2 = "2.wav"
FILE_3 = "3.wav"

def config_test_file(dir, filename):
    return dir + '/' + filename

test_file_1 = config_test_file(TEST_DIR, FILE_1)
test_file_2 = config_test_file(TEST_DIR, FILE_2)
test_file_3 = config_test_file(TEST_DIR, FILE_3)

wav_obj_1 = WaveObject(test_file_1)
wav_obj_2 = WaveObject(test_file_2)
wav_obj_3 = WaveObject(test_file_3)

test_group_1 = (wav_obj_1, wav_obj_2, wav_obj_3) # Group of valid wave files for testing
