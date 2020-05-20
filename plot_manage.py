from feature_extraction import *
from file_manage import *

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
    #ax[3, 0].set_ylabel('MFCC')

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

def plot_test_files():
    data1, sr1 = read_wave(test_file_1)
    data2, sr2 = read_wave(test_file_2)
    data3, sr3 = read_wave(test_file_3)
    data4, sr4 = read_wave(test_file_4)
    data5, sr5 = read_wave(test_file_5)

    f1 = FeatureObj(data1, sr1, test_file_1)
    print("Sample 1 done")
    f2 = FeatureObj(data2, sr2, test_file_2)
    print("Sample 2 done")
    f3 = FeatureObj(data3, sr3, test_file_3)
    print("Sample 3 done")
    f4 = FeatureObj(data4, sr4, test_file_4)
    print("Sample 4 done")
    f5 = FeatureObj(data5, sr5, test_file_5)
    print("Sample 5 done")

    plotFeatures([f1, f2, f3, f4, f5])

def plot_claps():
    clapData1, sr1 = read_wave(clap_file_1)
    clapData2, sr2 = read_wave(clap_file_2)
    clapData3, sr3 = read_wave(clap_file_3)
    clapData4, sr4 = read_wave(clap_file_4)
    clapData5, sr5 = read_wave(clap_file_5)

    f1 = FeatureObj(clapData1, sr1, clap_file_1)
    f2 = FeatureObj(clapData2, sr2, clap_file_2)
    f3 = FeatureObj(clapData3, sr3, clap_file_3)
    f4 = FeatureObj(clapData4, sr4, clap_file_4)
    f5 = FeatureObj(clapData5, sr5, clap_file_5)

    plotFeatures([f1, f2, f3, f4, f5])

def plot_crashes():
    crashData1, sr1 = read_wave(crash_file_1)
    crashData2, sr2 = read_wave(crash_file_2)
    crashData3, sr3 = read_wave(crash_file_3)
    crashData4, sr4 = read_wave(crash_file_4)
    crashData5, sr5 = read_wave(crash_file_5)

    f1 = FeatureObj(crashData1, sr1, crash_file_1)
    f2 = FeatureObj(crashData2, sr2, crash_file_2)
    f3 = FeatureObj(crashData3, sr3, crash_file_3)
    f4 = FeatureObj(crashData4, sr4, crash_file_4)
    f5 = FeatureObj(crashData5, sr5, crash_file_5)

    plotFeatures([f1, f2, f3, f4, f5])

def plot_hihats():
    hihatData1, sr1 = read_wave(hihat_file_1)
    hihatData2, sr2 = read_wave(hihat_file_2)
    hihatData3, sr3 = read_wave(hihat_file_3)
    hihatData4, sr4 = read_wave(hihat_file_4)
    hihatData5, sr5 = read_wave(hihat_file_5)

    f1 = FeatureObj(hihatData1, sr1, hihat_file_1)
    f2 = FeatureObj(hihatData2, sr2, hihat_file_2)
    f3 = FeatureObj(hihatData3, sr3, hihat_file_3)
    f4 = FeatureObj(hihatData4, sr4, hihat_file_4)
    f5 = FeatureObj(hihatData5, sr5, hihat_file_5)

    plotFeatures([f1, f2, f3, f4, f5])

plot_test_files()
plt.show()
