#############################################################################
# Module containing bjects to import and parse information from .wav files  #
# Reason for
#############################################################################

import struct as st

class Header:
    def __init__(self, contentString):
        self.chunkID       = contentString[0:4].decode('ascii') # Should read 'RIFF'
        self.chunkSize     = st.unpack('<L', contentString[4:8])[0] # Gives (file size - 8) (bytes)
        self.format        = contentString[8:12].decode('ascii') # Should read 'WAVE'
        self.subChunk1ID   = contentString[12:16].decode('ascii') # Should be 'fmt '
        self.subChunk1Size = st.unpack('<L', contentString[16:20])[0] # Gives remainder size of the subchunk
        self.audioFormat   = st.unpack('<H', contentString[20:22])[0] # 1 for PCM, NOTE: only handle these for now
        self.numChannels   = st.unpack('<H', contentString[22:24])[0] # 2 for stereo: NOTE: only handle these for now
        self.sampleRate    = st.unpack('<L', contentString[24:28])[0]
        self.byteRate      = st.unpack('<L', contentString[28:32])[0]
        self.blockAlign    = st.unpack('<H', contentString[32:34])[0]
        self.bitsPerSample = st.unpack('<H', contentString[34:36])[0]

    def __str__(self):
        return "\
        Chunk ID : {}\n\
        Chunk Size : {}\n\
        Format : {}\n\
        SubChunk 1 ID : {}\n\
        SubChunk 1 Size : {}\n\
        Audio Format : {}\n\
        Num Channels: {} \n\
        Sample Rate : {}\n\
        Byte Rate : {}\n\
        Block Align : {}\n\
        Bits Per Sample : {}\n\
        ".format(self.chunkID, \
        self.chunkSize, \
        self.format, \
        self.subChunk1ID, \
        self.subChunk1Size, \
        self.audioFormat, \
        self.numChannels, \
        self.sampleRate, \
        self.byteRate, \
        self.blockAlign, \
        self.bitsPerSample)

class Data:
    def __init__(self, dataString, bitsPerSample):
        self.subChunk2ID   = dataString[0:4].decode('ascii') # Should read 'data'
        self.subChunk2Size = st.unpack('<L', dataString[4:8])[0]

        bytesPerSample = bitsPerSample / 8
        self.frames = self.parse_data(int(bytesPerSample), dataString) # (leftChannel, rightChannel)
        self.avg = [(l + r) / 2 for l, r in zip(self.frames[0], self.frames[1])] # Mono data

    def __str__(self):
        return "\
        SubChunck 2 ID : {}\n\
        SubChunk 2 Size : {}\n\
        ".format(self.subChunk2ID, self.subChunk2Size)

    def parse_data(self, bytesPerSample, dataString):
        def convertBinaryStringToInt(bString): # For little endian format
            return int.from_bytes(bString, byteorder="little", signed=True)

        data = ([], []) # left channel data, right channel data
        pos = 8     # offset from begining of data string
        channel = 0 # start with left

        while pos < self.subChunk2Size:
            value = dataString[pos:pos+bytesPerSample]
            data[channel].append(convertBinaryStringToInt(value))
            channel = -~-channel # alternate between channel 1 and 0
            pos += bytesPerSample

        return data

class WaveObject:
    def __init__(self, filename, normalize=False, normLevel=None):
        self.filename = filename
        self.header   = None
        self.data     = None
        self.fileSize = None
        self.parse_file()

        if normalize:
            self.normalize_data(normLevel)

    def findDataStart(self, fileContent): # Find beginning of data chunk in case of malformed header
        start = 36
        while start < len(fileContent):
            if (fileContent[start:start+4] == b'data'):
                return start
            else:
                start += 1
        return None

    def parse_file(self):
        with open(self.filename, mode='rb') as file:
            fileContent = file.read()

        self.fileSize = len(fileContent)
        self.header = Header(fileContent)

        dataStart = self.findDataStart(fileContent)
        if dataStart == None:
            return

        self.data = Data(fileContent[dataStart:], self.header.bitsPerSample)

    def normalize_data(self, level):
        if level is not None:
            leftData = self.data.frames[0]
            rightData = self.data.frames[1]

            maxVal = abs(max(max(leftData, key=abs), max(rightData, key=abs), key=abs))
            multiplier = level / maxVal

            for i in range(len(leftData)):
                leftData[i] *= multiplier

            for i in range(len(rightData)):
                rightData[i] *= multiplier
