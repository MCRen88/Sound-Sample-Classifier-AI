#############################################
# Module to calculate features from         #
# audio objects                             #
#############################################
import numpy as np
import matplotlib.pyplot as plt
import math
from read_wave import *
from file_manage import *

class FeatureObj:
    def __init__(self, signal, sampleRate, filename):
        self.filename = filename[10:len(filename)-4]
        self.sampleRate = sampleRate
        self.signal = signal
        self.duration = len(self.signal) / self.sampleRate

        # Features:
        self.zeroCrossingRate = self.calcZeroCrossingrate() # float
        self.fft = self.calcFFT(self.signal)                # (response_y, frequency_x)
        self.filterBanks = self.calcFilterBanks()           #
        self.mfcc = self.calcMFCC()                         #

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
        frame_length = 0.02 # in seconds
        frame_offset = 0.005

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
        hiFreq = 10500
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
                filter_values.append(math.log(self.applyFilter(filter, frame), 10))

            filterBanks.append(filter_values)

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
        
        return


def plotFeatures(featureObjs):
    numCols = len(featureObjs) # show these along the horizontal (columns)
    numRows = 4 # Time domain, FFT, frequency banks, MFCC

    fig, ax = plt.subplots(nrows=numRows, ncols=numCols, sharey=False, figsize=(16, 9))

    plt.subplots_adjust(left=0.075, right=.975, top=0.9, bottom=0.05)
    fig.suptitle('Feature Plots')
    for i in range(numCols):
        ax[0, i].set_title(featureObjs[i].filename)

    ax[0, 0].set_ylabel('Time Domain')
    ax[1, 0].set_ylabel('FFT')
    ax[2, 0].set_ylabel('Filter Banks')
    ax[3, 0].set_ylabel('MFCC')

    for i in range(numCols):
        # Plot time domain signal
        frames = range(len(featureObjs[i].signal))
        time = [frame / featureObjs[i].sampleRate for frame in frames]
        ax[0, i].plot(time, featureObjs[i].signal, '#ff7878')
        ax[0, i].set_facecolor('#e0e0e0')

    for i in range(numCols):
        # Plot FFTs of entire signal
        ax[1, i].plot(featureObjs[i].fft[1], featureObjs[i].fft[0], '#ff7878')
        ax[1, i].set_facecolor('#e0e0e0')

    for i in range(numCols):
        # Plot Filter Banks
        ax[2, i].imshow(featureObjs[i].filterBanks, cmap='winter', interpolation='nearest', aspect='auto')

def plotFeature(featureObj):
    numRows = 4 # Time domain, FFT, frequency banks, MFCC

    fig, ax = plt.subplots(nrows=numRows, ncols=1, sharey=False, figsize=(16, 9))

    plt.subplots_adjust(left=0.075, right=.975, top=0.9, bottom=0.05)
    fig.suptitle('Feature Plots')

    ax[0].set_title(featureObj.filename)

    ax[0].set_ylabel('Time Domain')
    ax[1].set_ylabel('FFT')
    ax[2].set_ylabel('Filter Banks')
    ax[3].set_ylabel('MFCC')

    # Plot time domain signal
    frames = range(len(featureObj.signal))
    time = [frame / featureObj.sampleRate for frame in frames]
    ax[0].plot(time, featureObj.signal, '#ff7878')
    ax[0].set_facecolor('#e0e0e0')


    # Plot FFTs of entire signal
    ax[1].plot(featureObj.fft[1], featureObj.fft[0], '#ff7878')
    ax[1].set_facecolor('#e0e0e0')


    # Plot Filter Banks
    ax[2].imshow(featureObj.filterBanks, cmap='winter', interpolation='nearest', extend=[0, 100, 0, 1], aspect='auto')

# data1, sr1 = read_wave(test_file_1)
# data2, sr2 = read_wave(test_file_2)
# data3, sr3 = read_wave(test_file_3)
# data4, sr4 = read_wave(test_file_4)
# data5, sr5 = read_wave(test_file_5)
#
# data1 = trimData(data1, 0.001)
# data2 = trimData(data2, 0.001)
# data3 = trimData(data3, 0.001)
# data4 = trimData(data4, 0.001)
# data5 = trimData(data5, 0.001)
#
# f1 = FeatureObj(data1, sr1, test_file_1)
# print("Sample 1 done")
# f2 = FeatureObj(data2, sr2, test_file_2)
# print("Sample 2 done")
# f3 = FeatureObj(data3, sr3, test_file_3)
# print("Sample 3 done")
# f4 = FeatureObj(data4, sr4, test_file_4)
# print("Sample 4 done")
# f5 = FeatureObj(data5, sr5, test_file_5)
# print("Sample 5 done")
