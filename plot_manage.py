from feature_extraction import *
from file_manage import *


def plot_claps():
    clapData1, sr1 = read_wave(clap_file_1)
    clapData2, sr2 = read_wave(clap_file_2)
    clapData3, sr3 = read_wave(clap_file_3)
    clapData4, sr4 = read_wave(clap_file_4)
    clapData5, sr5 = read_wave(clap_file_5)

    clapData1 = trimData(clapData1, 0.0005)
    clapData2 = trimData(clapData2, 0.0005)
    clapData3 = trimData(clapData3, 0.0005)
    clapData4 = trimData(clapData4, 0.0005)
    clapData5 = trimData(clapData5, 0.0005)

    f1 = FeatureObj(clapData1, sr1, clap_file_1)
    print("Sample 1 done")
    f2 = FeatureObj(clapData2, sr2, clap_file_2)
    print("Sample 2 done")
    f3 = FeatureObj(clapData3, sr3, clap_file_3)
    print("Sample 3 done")
    f4 = FeatureObj(clapData4, sr4, clap_file_4)
    print("Sample 4 done")
    f5 = FeatureObj(clapData5, sr5, clap_file_5)
    print("Sample 5 done")

    plotFeatures([f1, f2, f3, f4, f5])

    plt.show()

plot_claps()
