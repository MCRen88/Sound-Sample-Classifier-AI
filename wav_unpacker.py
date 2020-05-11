import struct as st

class Header:
    def __init__(self, contentString):
        self.validFlag = None
        self.chunkID = contentString[0:4].decode('ascii') # Should read 'RIFF'
        self.chunkSize = st.unpack('<L', contentString[4:8])[0] # Gives file size - 8 (in bytes)
        self.format = contentString[8:12].decode('ascii') # Should read 'WAVE'
        self.subChunk1ID = contentString[12:16].decode('ascii') # Should be 'fmt '
        self.subChunk1Size = st.unpack('<L', contentString[16:20])[0] # Gives remainder size of the subchunk
        self.audioFormat = st.unpack('<H', contentString[20:22])[0] # 1 for PCM, NOTE: only handle these for now
        self.numChannels = st.unpack('<H', contentString[22:24])[0] # 2 for stereo: NOTE: only handle these for now
        self.sampleRate = st.unpack('<L', contentString[24:28])[0]
        self.byteRate = st.unpack('<L', contentString[28:32])[0]
        self.blockAlign = st.unpack('<H', contentString[32:34])[0]
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
        self.validFlag = None
        self.subChunk2ID = dataString[0:4].decode('ascii') # Should read 'data'
        self.subChunk2Size = st.unpack('<L', dataString[4:8])[0]

        bytesPerSample = bitsPerSample / 8
        self.frames = self.parse_data(int(bytesPerSample), dataString)

    def __str__(self):
        return "\
        SubChunck 2 ID : {}\n\
        SubChunk 2 Size : {}\n\
        ".format(self.subChunk2ID, self.subChunk2Size)

    def parse_data(self, bytesPerSample, dataString):
        def convertBinaryStringToInt(bString): # For little endian format
            return int.from_bytes(bString, byteorder="little", signed=False)

        data = ([], []) # left channel data, right channel data
        pos = 8
        channel = 0 # start with left

        while pos < self.subChunk2Size:
            value = dataString[pos:pos+bytesPerSample]
            data[channel].append(convertBinaryStringToInt(value))
            channel = -~-channel # alternate between channel 1 and 0
            pos += bytesPerSample

        return data

class WaveObject:
    def __init__(self, filename):
        self.filename = filename
        self.header   = None
        self.data     = None
        self.fileSize = None
        self.parse_file()

    def findDataStart(self, fileContent):
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
        self.data = Data(fileContent[dataStart:], self.header.bitsPerSample)
