import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import math

dataSet = [[256, 0.4140012264251709], [512, 1.4179987907409668], [1024, 5.595750570297241], [2048, 21.421449899673462], [4096, 84.26186633110046], [8192, 341.21426653862], [16384, 1406.4262495040894], [29848, 4667.0919942855835]]

def graphTimings(timings):
    sizes = [timings[x][0] for x in range(len(timings))]
    times = [timings[x][1] for x in range(len(timings))]
    timesPredicted = [5.144175652772087 * 1.0002744824690908 ** n for n in sizes]

    plt.plot(sizes, times, "g", label="Dyanmic Programming Alignment Algorithm")
    plt.plot(sizes, timesPredicted, "r", label="Prediciton")
    plt.title("Runtime of DNA Alignment Algorithm vs Size of Sequences")
    plt.xlabel("Size of Sequence")
    plt.ylabel("Time in Seconds")
    plt.yscale('log')
    plt.rcParams["figure.figsize"] = [16, 9]
    plt.legend()
    plt.show()

    slope, intercept, _, _, _ = stats.linregress([sizes], [math.log(t) for t in times])

    print(slope, intercept)

    print("time = %.10f * %.10f ^ n" % (np.exp(intercept), np.exp(slope)))

graphTimings(dataSet)