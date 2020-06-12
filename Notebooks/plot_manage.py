from feature_extraction import *
from file_manage import *
from tqdm import tqdm
import matplotlib.pyplot as plt

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
        pos = ax[2, i].imshow(featureObjs[i].filterBanks, cmap='winter', interpolation='nearest', aspect='auto')
        fig.colorbar(pos, ax=ax[2, i])

    for i in range(numCols):
        # Plot MFCCs
        pos = ax[3, i].imshow(featureObjs[i].mfcc, cmap='winter', interpolation='nearest', aspect='auto')
        fig.colorbar(pos, ax=ax[3, i])


def configFeaturesToPlot(nameList, progressBar):
    featureList = []
    if progressBar:
        for name in tqdm(nameList):
            data, sr = read_wave(name)
            f = FeatureObj(data, sr, name)
            featureList.append(f)
    else:
        for name in nameList:
            data, sr = read_wave(name)
            f = FeatureObj(data, sr, name)
            featureList.append(f)
    return featureList

def plot_test_files(progressBar=True):
    f = configFeaturesToPlot([test_file_1,
                              test_file_2,
                              test_file_3,
                              test_file_4,
                              test_file_5], progressBar)
    plotFeatures(f)

def plot_claps(progressBar=True):
    f = configFeaturesToPlot([clap_file_1,
                              clap_file_2,
                              clap_file_3,
                              clap_file_4,
                              clap_file_5], progressBar)
    plotFeatures(f)

def plot_crashes(progressBar=True):
    f = configFeaturesToPlot([crash_file_1,
                              crash_file_2,
                              crash_file_3,
                              crash_file_4,
                              crash_file_5], progressBar)
    plotFeatures(f)

def plot_hihats(progressBar=True):
    f = configFeaturesToPlot([hihat_file_1,
                              hihat_file_2,
                              hihat_file_3,
                              hihat_file_4,
                              hihat_file_5], progressBar)
    plotFeatures(f)

def plot_kicks(progressBar=True):
    f = configFeaturesToPlot([kick_file_1,
                              kick_file_2,
                              kick_file_3,
                              kick_file_4,
                              kick_file_5], progressBar)
    plotFeatures(f)

def plot_snares(progressBar=True):
    f = configFeaturesToPlot([snare_file_1,
                              snare_file_2,
                              snare_file_3,
                              snare_file_4,
                              snare_file_5], progressBar)
    plotFeatures(f)

if __name__ == '__main__':
    plot_snares()
    plt.show()
