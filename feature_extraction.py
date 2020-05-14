#############################################
# Module to calculate features from         #
# audio objects                             #
#############################################

from wav_unpacker import *

class FeatureObj:
    def __init__(self, wavObj):
        self.wavObj = wavObj
        self.zeroCrossingRate = self.calcZeroCrossingrate()

    def.calcZeroCrossingrate(self):
        # Formula from : https://en.wikipedia.org/wiki/Zero-crossing_rate
        data = self.wavObj.data.avg
        T = len(data)
        numCrossings = 0

        for t in range(1, T):
            if data[t] * data[t-1] < 0:
                numCrossings += 1

        return numCrossings / T
