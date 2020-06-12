#############################################
# Module to calculate features from         #
# audio objects                             #
#############################################
import numpy as np
import math
from read_wave import *
from file_manage import *
from scipy.fftpack import dct
import random

class FeatureObj:
    def __init__(self, signal, sampleRate, filename):
        self.filename = filename[10:len(filename)-4]
        self.sampleRate = sampleRate
        self.signal = signal
        self.duration = len(self.signal) / self.sampleRate

        # Features:
        self.zeroCrossingRate = self.calcZeroCrossingrate()
        self.fft = self.calcFFT(self.signal)
        self.filterBanks = self.calcFilterBanks()
        self.mfcc = self.calcMFCC()

    def calcZeroCrossingrate(self):
        # Formula from : https://en.wikipedia.org/wiki/Zero-crossing_rate
        data = self.signal
        T = len(data)
        numCrossings = 0

        for t in range(1, T):
            if data[t] * data[t-1] < 0:
                numCrossings += 1

        return numCrossings / T

    def mel(self, f):
        return 2595 * math.log(1 + f / 700, 10)

    def imel(self, m):
        return 700 * (10**(m/2595) - 1)

    def applyFilter(self, filter, frame):
        lb = filter[0]
        m = filter[1]
        ub = filter[2]

        values = frame[0]
        freqs = frame[1]

        total = 0

        for i in range(len(freqs)):
            if freqs[i] < lb:
                total += 0
            elif freqs[i] > lb and freqs[i] <= m:
                slope = 1 / (m - lb)
                scale = slope * (freqs[i] - lb)
                total += scale * values[i]
            elif freqs[i] > m and freqs[i] < ub:
                slope = 1 / (m - ub)
                scale = slope * (freqs[i] - ub)
                total += scale * values[i]
            else:
                total += 0
        return total

    def calcFFT(self, signal):
        freq = np.fft.rfftfreq(len(signal), d=1/self.sampleRate)
        full_fft = np.fft.rfft(signal)
        response = abs(full_fft / len(full_fft)) # normalize (can also try len(full_fft) or max(abs(full_fft)))
        return (response, freq)

    def calcFilterBanks(self):
        ''' SAMPLING FRAMES '''
        frame_length = 0.025 # in seconds
        frame_offset = 0.01

        samplesPerFrame = math.ceil(self.sampleRate * frame_length)
        offsetPerFrame =  math.ceil(self.sampleRate * frame_offset)

        frames = [] # contains segments of audio data
        lb = 0
        ub = lb + samplesPerFrame
        while True:
            if lb > len(self.signal):
                break

            if ub < len(self.signal):
                frames.append(self.signal[lb:ub])

            else:
                remainder = self.signal[lb:]
                padding = [0] * (samplesPerFrame - len(remainder))
                remainder.extend(padding)
                frames.append(remainder)

            lb += offsetPerFrame
            ub = lb + samplesPerFrame

        ''' CALCULATE SHORT TIME FFT '''
        fft_frames = [] # FFT over all segments

        for frame in frames:
            fft_frames.append(self.calcFFT(frame))

        ''' GENERATE TRIANGULAR FILTERS '''
        lowFreq = 300
        hiFreq = 10000
        numFilters = 26

        lowMel = self.mel(lowFreq)
        hiMel = self.mel(hiFreq)

        melSpacing = (hiMel - lowMel) / (numFilters + 1)
        melFilterDivisions = [lowMel + x * melSpacing for x in range(numFilters + 2)]
        freqFilterDivisions = [math.floor(self.imel(x)) for x in melFilterDivisions]

        filters = [(freqFilterDivisions[i-1], freqFilterDivisions[i],freqFilterDivisions[i+1]) for i in range(1, numFilters + 1)]

        ''' APPLY FILTERS OVER FFT FRAMES '''
        filterBanks = []

        for frame in fft_frames:
            filter_values = []
            for filter in filters:
                value = self.applyFilter(filter, frame)
                if value == 0:
                    filter_values.append(float("inf"))
                else:
                    filter_values.append(20 * math.log(value, 10))

            overallMin = min(filter_values)
            for i in range(len(filter_values)):
                if filter_values[i] == float("inf"):
                    filter_values[i] = overallMin

            filterBanks.append(filter_values)


        framesDesired = 75

        if len(filterBanks) < framesDesired:
            start = len(filterBanks) - 1
            filterBanks = np.append(filterBanks, [filterBanks[-1]] * (framesDesired - len(filterBanks)), 0)

            endValue = min(filterBanks[-1])

            for i in range(26):
                startValue = filterBanks[start, i]
                multiplier = (endValue - startValue) / (framesDesired - start)

                c = 0
                for j in range(start, framesDesired):
                    filterBanks[j, i] += c * multiplier + random.uniform(-1, 1)
                    c +=1

        elif len(filterBanks) > framesDesired:
            filterBanks = filterBanks[:framesDesired]

        return np.transpose(filterBanks)


    def calcMFCC(self):
        '''
        Algorithm: http://practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/
        1. get time frames of time domain signal (20 ms in length, each frame offset by around 10 ms)
        2. On each time frame, perform FFT, and retrive the absolute value normalized (same as regular FFT)
           Now we have the FFTs of many frames of audio data over time, we'll call them fft_frames
        3. For each fft_frame, compute the Mel-spaced filterbank (26 total).
                a. Set lower and upper bounds on the range of frequencies (eg. 300 Hz to 10,000 Hz)
                b. Convert the bounds to mels
                c. If we use 26 filters, we will need 28 equally spaced points between the mel bounds
                d. Convert the 28 points back to Hz
                e. Filters are built using these points now, each ranges three points.
                   eg. Filter 1: (p1: 0, p2: 1, p3: 0) Filter 2: (p2: 0, p3: 1, p4: 0)
                   To do this, we need to calculate lines between points to form triangular filters
                f. Apply the each filter over the fft_frame by multiplying the corresponding frequencies
                   and add up the coefficients.
                g. Take the log of each of the 26 coefficients to get filterbank energies
                h. Take DCT of each energy to get MFCC (only keep the lower 13)
        '''
        mfcc = np.transpose(self.filterBanks.copy())
        mfcc = dct(mfcc, type=2, axis=1, norm='ortho')[:,:13]
        return np.transpose(mfcc)
