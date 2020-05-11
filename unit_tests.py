from util import *
import sys
import inspect


def test_header_group(wav_objects): # Test Header consistency
    for wav_object in wav_objects:
        try:
            assert wav_object.header.chunkID == 'RIFF'
            assert wav_object.header.chunkSize == wav_object.fileSize - 8
            assert wav_object.header.format == 'WAVE'
            assert wav_object.header.subChunk1ID == 'fmt '
            assert wav_object.header.byteRate == wav_object.header.sampleRate * wav_object.header.numChannels * wav_object.header.bitsPerSample / 8
            assert wav_object.header.blockAlign == wav_object.header.numChannels * wav_object.header.bitsPerSample / 8

        except AssertionError:
            print(str_red("Test [{}] Failed on line {}").format(inspect.stack()[0][3], sys.exc_info()[-1].tb_lineno))
            return

    print(str_green("Test [{}] Passed").format(inspect.stack()[0][3]))

def test_data_group(wav_objects): # Test Data and general frame consistency
    for wav_object in wav_objects:
        try:
            assert wav_object.data.subChunk2ID == 'data'
            assert len(wav_object.data.frames[0]) == len(wav_object.data.frames[1])

        except AssertionError:
            print(str_red("Test [{}] Failed on line {}").format(inspect.stack()[0][3], sys.exc_info()[-1].tb_lineno))
            return

    print(str_green("Test [{}] Passed").format(inspect.stack()[0][3]))

def test_data_1(wav_object): # Specific sample tests via reading data from hex-view
    try:
        assert wav_object.data.frames[0][0] == 3879648
        assert wav_object.data.frames[1][0] == 3729040

        assert wav_object.data.frames[0][1] == 2110816
        assert wav_object.data.frames[1][1] == 2045504

        assert wav_object.data.frames[0][2] == 4237072
        assert wav_object.data.frames[1][2] == 4273760

    except AssertionError:
        print(str_red("Test [{}] Failed on line {}").format(inspect.stack()[0][3], sys.exc_info()[-1].tb_lineno))
        return

    print(str_green("Test [{}] Passed").format(inspect.stack()[0][3]))

def test_data_2(wav_object): # Specific sample tests via reading data from hex-view
    try:
        assert wav_object.data.frames[0][0] == 1471
        assert wav_object.data.frames[1][0] == 1753

        assert wav_object.data.frames[0][1] == 1679
        assert wav_object.data.frames[1][1] == 1594

        assert wav_object.data.frames[0][2] == 1920
        assert wav_object.data.frames[1][2] == 1440

    except AssertionError:
        print(str_red("Test [{}] Failed on line {}").format(inspect.stack()[0][3], sys.exc_info()[-1].tb_lineno))
        return

    print(str_green("Test [{}] Passed").format(inspect.stack()[0][3]))

def test_data_3(wav_object): # Specific sample tests via reading data from hex-view
    try:
        assert wav_object.data.frames[0][0] == 2
        assert wav_object.data.frames[1][0] == 2

        assert wav_object.data.frames[0][1] == 1
        assert wav_object.data.frames[1][1] == 65535

        assert wav_object.data.frames[0][2] == 1
        assert wav_object.data.frames[1][2] == 2

    except AssertionError:
        print(str_red("Test [{}] Failed on line {}").format(inspect.stack()[0][3], sys.exc_info()[-1].tb_lineno))
        return

    print(str_green("Test [{}] Passed").format(inspect.stack()[0][3]))
