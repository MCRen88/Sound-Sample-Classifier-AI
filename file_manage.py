#####################################
# Module to streamline file access  #
#####################################
DIR = "wav_files"
FILE_1 = "edm-clap-01.wav"
FILE_2 = "edm-crash-04.wav"
FILE_3 = "edm-hihat-12.wav"
FILE_4 = "edm-kick-08.wav"
FILE_5 = 'A5.wav' #880 Hz

def config_test_file(dir, filename):
    return dir + '/' + filename

test_file_1 = config_test_file(DIR, FILE_1)
test_file_2 = config_test_file(DIR, FILE_2)
test_file_3 = config_test_file(DIR, FILE_3)
test_file_4 = config_test_file(DIR, FILE_4)
test_file_5 = config_test_file(DIR, FILE_5)


clap_file_1 = config_test_file(DIR+'/Claps', '1.wav')
clap_file_2 = config_test_file(DIR+'/Claps', '2.wav')
clap_file_3 = config_test_file(DIR+'/Claps', '3.wav')
clap_file_4 = config_test_file(DIR+'/Claps', '4.wav')
clap_file_5 = config_test_file(DIR+'/Claps', '5.wav')
