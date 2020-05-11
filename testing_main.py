from wav_unpacker import *
import unit_tests

TEST_DIR = "wav_files"
FILE_1 = "1.wav"
FILE_2 = "2.wav" # problematic file format
FILE_3 = "3.wav"

def config_test_file(dir, filename):
    return dir + '/' + filename

test_file_1 = config_test_file(TEST_DIR, FILE_1)
test_file_2 = config_test_file(TEST_DIR, FILE_2)
test_file_3 = config_test_file(TEST_DIR, FILE_3)

test_obj_1 = WaveObject(test_file_1)
test_obj_2 = WaveObject(test_file_2)
test_obj_3 = WaveObject(test_file_3)
test_group_1 = (test_obj_1, test_obj_2, test_obj_3) # Group of valid wave files




unit_tests.test_header_group(test_group_1)
unit_tests.test_data_group(test_group_1)

#unit_tests.test_data_1(test_obj_1)
#unit_tests.test_data_2(test_obj_2)
# unit_tests.test_data_3(test_obj_3)

#print(test_obj_2.header)
# print(test_obj_2.header)
# print(test_obj_3.header)
