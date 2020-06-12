import numpy as np
import math
import random

def get_spectrogram(signal, sr,
                    frame_length=0.025, frame_offset=0.01,
                    lowFreq=300, hiFreq=10000,
                    numFilters=26, numFrames=75):
    '''
    Inputs: signal (list)        - mono normalized audio data
            sr (int)             - sample rate (Hz)
            frame_length (float) - time alloted for each spectogram frame (sec)
            frame_offset (float) - time between adjacent frames (sec)
            lowFreq (float)      - lower bound for filters (Hz)
            hiFreq (float)       - upper bound for filters (Hz)
            numFilters (int)     - number of filters to describe data
            numFrames (int)      - desired number of output frames, if true number of frames analyzed is greater than
                                   numFrames, then it will be truncated. If true number of frames analyzed is
                                   less than numFrames, additional gradient frames will be appended.


    Outputs: numFilters x numFrames numpy array which can be plotted directly to show the spectogram representation of the input signal
             axis 0 = numFilters
             axis 1 = numFrames

    Helper Functions
    '''
    def _mel(f):
        '''Convert Hz to Mels'''
        return 2595 * math.log(1 + f / 700, 10)

    def _imel(m):
        '''Convert Mels to Hz'''
        return 700 * (10**(m/2595) - 1)

    def _applyFilter(filter, frame):
        ''' Apply a triangular filter over a frame of data'''
        lb = filter[0] # Bounds of the triangular filter
        m = filter[1]
        ub = filter[2]

        values = frame[0] # values from the FFT
        freqs = frame[1]

        total = 0

        for i in range(len(freqs)):
            if freqs[i] < lb: # out of filter range
                total += 0
            elif freqs[i] > lb and freqs[i] <= m: # On the rising edge of the filter
                slope = 1 / (m - lb)
                scale = slope * (freqs[i] - lb)
                total += scale * values[i]
            elif freqs[i] > m and freqs[i] < ub: # On the falling edge of the filter
                slope = 1 / (m - ub)
                scale = slope * (freqs[i] - ub)
                total += scale * values[i]
            else:  # out of filter range
                total += 0
        return total

    def _calcFFT(signal, sr):
        ''' Perform FFT on a signal and return the appropriate axes '''
        freq = np.fft.rfftfreq(len(signal), d=1/sr)
        full_fft = np.fft.rfft(signal)
        response = abs(full_fft / len(full_fft))
        return (response, freq)


    ''' Create audio frames '''
    samplesPerFrame = math.ceil(sr * frame_length)
    offsetPerFrame =  math.ceil(sr * frame_offset)

    frames = []
    lb = 0
    ub = lb + samplesPerFrame

    while True:
        if lb > len(signal):
            break

        if ub < len(signal):
            frames.append(signal[lb:ub])

        else:
            remainder = signal[lb:]
            padding = [0] * (samplesPerFrame - len(remainder))
            remainder.extend(padding)
            frames.append(remainder)

        lb += offsetPerFrame
        ub = lb + samplesPerFrame

    ''' Apply FFT over audio frames '''
    fft_frames = []

    for frame in frames:
        fft_frames.append(_calcFFT(frame, sr))

    ''' Generate list of triangular filters, in which each filter is denoted by
        a tuple of 3 frequency points that define the vertices of the filter '''
    lowMel = _mel(lowFreq)
    hiMel = _mel(hiFreq)

    melSpacing = (hiMel - lowMel) / (numFilters + 1)
    melFilterDivisions = [lowMel + x * melSpacing for x in range(numFilters + 2)]
    freqFilterDivisions = [math.floor(_imel(x)) for x in melFilterDivisions]

    filters = [(freqFilterDivisions[i-1], freqFilterDivisions[i],freqFilterDivisions[i+1]) for i in range(1, numFilters + 1)]

    ''' Apply filters over the fft_frames to get filterbanks '''
    filterBanks = []

    for frame in fft_frames:
        filter_values = []
        for filter in filters:
            value = _applyFilter(filter, frame)
            if value == 0:
                filter_values.append(float("inf"))
            else:
                filter_values.append(20 * math.log(value, 10))

        overallMin = min(filter_values) # Replace any "inf" values with the min filter value of the frame
        if overallMin == float('inf'):
            pass
        else:
            for i in range(len(filter_values)):
                if filter_values[i] == float("inf"):
                    filter_values[i] = overallMin

            filterBanks.append(filter_values)

    ''' Apply a gradient appended at the end of short audio files or cut off long audio samples '''
    if len(filterBanks) < numFrames:
        start = len(filterBanks) - 1
        filterBanks = np.append(filterBanks, [filterBanks[-1]] * (numFrames - len(filterBanks)), 0)
        endValue = min(filterBanks[-1])

        for i in range(numFilters):
            startValue = filterBanks[start, i]
            multiplier = (endValue - startValue) / (numFrames - start)

            c = 0
            for j in range(start, numFrames):
                filterBanks[j, i] += c * multiplier + random.uniform(-1, 1)
                c += 1

    elif len(filterBanks) > numFrames:
        filterBanks = filterBanks[:numFrames]

    filterBanks = np.array(filterBanks)
    scale = abs(max(filterBanks.min(), filterBanks.max(), key=abs))
    filterBanks = filterBanks / scale

    return np.transpose(filterBanks)
