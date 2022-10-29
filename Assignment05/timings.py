import random
from closestpoints import close, closestPair, closestPairY, closestPairMerge, closestPairMergeR
from testpoints import createProblem
import math
import numpy as np
import time
from scipy import stats
import matplotlib.pyplot as plt

"""
Generates Timing Data for Different Multiplication Functions testing on Varying Problem Sizes
functions: List of Functions to Time, Each of Which Takes two Lists of Integers and Multiplies Them Together
start: Starting Problem Size (Must be a Power of 2)
end: Ending Problem Size (Must be a Power of 2)
problems: Number of Problems to Test for Each Problem Size
v: Verbose Mode
cutoff: Includes Only the First Function After This Point
includePython: Toggle to Include Python Built-in
Returns: List of List of Points, One List Per Function
"""


def timePointFunctions(functions, generator, start, stop, problems=10, v=False):
    assert math.log(start) / math.log(2) % 1 == 0
    assert math.log(stop) / math.log(2) % 1 == 0
    maxIter = int(math.log(stop / start) / math.log(2)) + 1

    n = start
    timings = [[] for i in range(len(functions))]

    for i in range(maxIter):
        if v:
            print(f"Running Tests for Size n={n}")

        # Generates problems Random Problems
        problemSet = [generator(n) for i in range(problems)]

        for j in range(len(functions)):
            startTime = time.time()
            for k in range(problems):
                functions[j](problemSet[k], n)
            timings[j].append((n, (time.time() - startTime) / problems))

        n *= 2

    return timings


"""
Parses the Data from the Timing Function Into a Graph
timings: Timing Data
names: Names of Functions Timed
"""


def graphTiming(timings, names):
    assert len(timings) == len(names)

    colors = ['r', 'g', 'y', 'b', 'o']

    for i in range(len(names)):
        slope, intercept, _, _, _ = stats.linregress([(safeLog(n), safeLog(k)) for n, k in timings[i]])
        print(f"{names[i]}: time = {np.exp(intercept):.8f} * n ^ {slope:.8f}")

    for i in range(len(names)):
        x, y = zip(*timings[i])
        plt.plot(x, y, colors[i], label=f"{names[i]}")

    plt.title("Runtime of Various Closet Point Algorithms vs Problem Size")
    plt.xlabel("Problem Size (Number of Points)")
    plt.ylabel("Time to Solve (Average)")
    plt.yscale('log')
    plt.xscale('log')
    plt.rcParams["figure.figsize"] = [16, 9]
    plt.legend()
    plt.show()


"""
Tests if the FFT Holds Accurately For Large Numbers at Varying Problem Sizes
start: Smallest Problem Size (Must be a Power of 2)
stop: Largest Problem Size (Must be a Power of 2)
problems: Tests to Run per Problem Size
v: Verbose Mode
returns: If the FFT Was Accurate All the Way Through
"""




def safeLog(a):
    if a == 0:
        return -1000
    return math.log(a)


if __name__ == "__main__":
    timings = timePointFunctions([close, closestPair, closestPairY, closestPairMerge], createProblem, 2**5, 2**12, v=True)
    graphTiming(timings, ["Schoolbook Algorithm", "Recursive Algorithm", "Y-Sort Algorithm", "MergeSort Algorithm"])

