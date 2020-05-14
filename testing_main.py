###############################
# Call unit tests from here   #
###############################

from wav_unpacker import *
import unit_tests
from file_manage import *

unit_tests.test_header_group(test_group_1)
unit_tests.test_data_group(test_group_1)

unit_tests.test_data_1(wav_obj_1)
unit_tests.test_data_2(wav_obj_2)
unit_tests.test_data_3(wav_obj_3)

# print(wav_obj_2.header)
# print(wav_obj_2.header)
# print(wav_obj_3.header)
