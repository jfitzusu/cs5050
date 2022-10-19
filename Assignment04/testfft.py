from fft import PQ_school, PQ_FFT, FFT
import random
import math
import numpy as np
import time
from scipy import stats
import matplotlib.pyplot as plt



"""
Function to Convert from a Given Base to Base 10
digits: Number Represented in Base base as an Array of Integers
base: Base to Convert From
"""
def convertBack(digits, base = 2 ** 12):
    # Initialize result
    digits = list(reversed(digits)) #start at the highest order term
    result = digits[0]
    # Evaluate value of polynomial
    # using Horner's method
    for i in range(1, len(digits)):
        result = result * base + digits[i]
    return result


"""
Function to Generate a Random Number in a Given Base Represented by a List of Integers
n: Number of Indexes to Generate (Must be a Power of 2)
k: Base
returns: List of Random Integers from 0 to k-1 of Length n
"""


def randomBaseK(n, k=2 ** 12):
    assert math.log(n) / math.log(2) % 1 == 0;
    return [random.randint(0, k - 1) for i in range(n)]


def testFFT(n, s=16, v=False):
    for i in range(n):
        P = randomBaseK(s)
        Q = randomBaseK(s)
        PQschool = PQ_school(P, Q)
        PQfft = PQ_FFT(P, Q)
        if v:
            print(f"School Algorithm:{PQschool}")
            print(f"FFT Algorithm   :{PQfft}")
        for i in range(len(PQschool)):
            if PQschool[i] != PQfft[i]:
                return True
    return True

"""
Generates Timing Data for Different Multiplication Functions testing on Varying Problem Sizes
functions: List of Functions to Time, Each of Which Takes two Lists of Integers and Multiplies Them Together
start: Starting Problem Size (Must be a Power of 2)
end: Ending Problem Size (Must be a Power of 2)
problems: Number of Problems to Test for Each Problem Size
"""
def timeMultiplicationFunctions(functions, start, stop, problems=10):
    assert math.log(start) / math.log(2) % 1 == 0
    assert math.log(stop) / math.log(2) % 1 == 0
    maxIter = int(math.log(stop / start) / math.log(2)) + 1

    n = start
    timings = np.zeros((maxIter, len(functions) + 1))

    # Initialize Size Values
    for i in range(len(timings)):
        timings[i][0] = n
        n *= 2

    for i in range(maxIter):
        # Generates problems Random Problems
        numberSet = [(randomBaseK(n), randomBaseK(n)) for i in range(problems)]

        for j in range(len(functions)):
            startTime = time.time()
            for k in range(problems):
                functions[j](numberSet[k][0], numberSet[k][1])
            timings[i][j + 1] = time.time() - startTime

        n *= 2

    return timings

def graphTiming(timings, names):
    assert len(timings[0]) == len(names)

    colors = ['r', 'g', 'y', 'b', 'o']

    sizes = [timings[i][0] for i in range(len(timings))]

    results = []
    for i in range(1, len(timings[0])):
        results.append([])
        for j in range(len(timings)):
            results[i].append(timings[j][i])


    for i in range(len(names)):
        slope, intercept, _, _, _ = stats.linregress([math.log(n) for n in sizes], [math.log(t) for t in results[i]])
        print(f"{names[i]}: time = {np.exp(intercept):.8f} * n ^ {slope:.8f}")

    for i in range(len(names)):
        plt.plot(sizes, results[i], colors[i], lable=f"{names[i]}")


    plt.title("Runtime of Various Multiplication Algorithms vs Problem Size (Base 2**12)")
    plt.xlabel("Size of Numbers (Number of Digits)")
    plt.ylabel("Time to Solve (10 Problems)")
    plt.yscale('log')
    plt.xscale('log')
    plt.rcParams["figure.figsize"] = [16, 9]
    plt.legend()
    plt.show()