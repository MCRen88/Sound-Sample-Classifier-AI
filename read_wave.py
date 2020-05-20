import struct as st
import numpy as np
import math

def read_wave(path, normalize=True, length=1, threshold=0.001):
    '''
    Function to parse wave file data.
    Inputs: path (string)    - full filepath to audio file
            normalize (bool) - set true to apply a normalization multiplier across audio frames
                               so that frame data ranges between [-1, 1]
            length (float)   - chops audio sample to meet this length (seconds). If audio sample is shorter than
                               length, it will be unchanged


    Outputs: data (list)  - array containing audio data values averaged between the left and right channels
             sampleRate (int) - 1 / sampleRate gives the time seperation between data values. sampleRate / 2 gives the
                                nyquist frequency of the discrete signal
    Return values are None, None if:
        1. File open error
        2. File not does meet the following specification:
            a. Correctly formed header information (chunk ids, formats, etc.)
            b. File is uncompressed (PCM = 1)
            c. File is stereo
    '''
    ''' HELPER FUNCTIONS START'''

    def _findDataStart(fileContent):
        start = 36
        while start < len(fileContent):
            if (fileContent[start:start+4] == b'data'):
                return start
            else:
                start += 1
        return None

    def _normalizeData(data):
        maxVal = abs(max(data, key=abs))
        multiplier = 1 / maxVal

        normalizedData = [x * multiplier for x in data]
        return normalizedData

    def _convertBinaryStringToInt(bString):
        return int.from_bytes(bString, byteorder="little", signed=True)

    def _extractData(dataString, bytesPerSample):
        size = st.unpack('<L', dataString[4:8])[0]
        pos = 8
        data = []

        while pos < size:
            leftData = _convertBinaryStringToInt(dataString[pos:pos+bytesPerSample])
            pos += bytesPerSample
            rightData = _convertBinaryStringToInt(dataString[pos:pos+bytesPerSample])
            pos += bytesPerSample
            data.append((leftData + rightData) / 2)

        return data

    def _applyLength(signal, sampleRate, duration):
        numFramesDesired = math.floor(sampleRate * duration)
        currNumFrames = len(signal)

        if currNumFrames > numFramesDesired:
            signal = signal[:numFramesDesired]

        return signal

    def _trimData(signal, threshold):
        windowSize = 100
        toTrim = [] # list of indeces to trim out of the signal

        absSignal = [abs(x) for x in signal]

        for i in range(len(absSignal)-windowSize):
            avg = sum(absSignal[i:i+windowSize]) / windowSize
            if avg < threshold:
                toTrim.append(i)

        for i in range(len(absSignal)-windowSize, len(absSignal)):
            avg = sum(absSignal[i:]) / len(signal[i:])
            if avg < threshold:
                toTrim.append(i)

        for idx in sorted(toTrim, reverse=True):
            del signal[idx]

        return signal
        ''' HELPER FUNCTIONS END'''

    try:
        with open(path, mode='rb') as file:
            fileContent = file.read()
    except:
        print("Cannot open file at: " + path)
        return None, None

    chunkID       = fileContent[0:4].decode('ascii') # Should read 'RIFF'
    format        = fileContent[8:12].decode('ascii') # Should read 'WAVE'
    subChunk1ID   = fileContent[12:16].decode('ascii') # Should be 'fmt '
    audioFormat   = st.unpack('<H', fileContent[20:22])[0] # 1 for PCM, NOTE: only handle this for now
    numChannels   = st.unpack('<H', fileContent[22:24])[0] # 2 for stereo, 1 for mono, if it is mono then left and right channel
                                                           # data are duplicated in each sample frame
    sampleRate    = st.unpack('<L', fileContent[24:28])[0]

    bitsPerSample = st.unpack('<H', fileContent[34:36])[0]

    if chunkID != 'RIFF' or format != 'WAVE' or subChunk1ID != 'fmt ' or audioFormat != 1 or (numChannels != 1 and numChannels != 2):
        print("File format issues at: " + path)
        print("Make sure file is not compressed")
        return None, None

    dataStart = _findDataStart(fileContent)
    if dataStart == None:
        print("File data could not be retrived at: " + path)
        return None, None

    bytesPerSample = bitsPerSample / 8
    if bytesPerSample.is_integer() == False:
        print("Imcompatiable bytes per sample at: " + path)
        return None, None

    data = _extractData(fileContent[dataStart:], int(bytesPerSample))

    if normalize:
        data = _normalizeData(data)

    if threshold is not None:
        data = _trimData(data, threshold)

    if length is not None:
        data = _applyLength(data, sampleRate, length)

    return data, sampleRate
