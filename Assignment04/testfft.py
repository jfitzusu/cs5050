from fft import PQ_school, PQ_FFT, FFT, mult3
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


"""
Test Code to Seee if the FFT Code Works, Using the School Algorithm as a Reference
n: Number of Problemst to Test
s: Problem Size
v: Verbose Mode
"""
def testFFTWorks(n, s=16, v=False):
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
v: Verbose Mode
cutoff: Includes Only the First Function After This Point
includePython: Toggle to Include Python Built-in
Returns: List of List of Points, One List Per Function
"""
def timeMultiplicationFunctions(functions, start, stop, problems=10, v=False, cutoff=math.inf, includePython=False):
    assert math.log(start) / math.log(2) % 1 == 0
    assert math.log(stop) / math.log(2) % 1 == 0
    maxIter = int(math.log(stop / start) / math.log(2)) + 1

    n = start
    timings = [[] for i in range(len(functions) + includePython)]

    for i in range(maxIter):
        if v:
            print(f"Running Tests for Size n={n}")

        # Only Evaluates the Fastest Algorithm After a Cutoff
        if n > cutoff:
            functions = [functions[0]]

        # Generates problems Random Problems
        numberSet = [(randomBaseK(n), randomBaseK(n)) for i in range(problems)]

        if includePython:
            pythonSet = [(convertBack(a), convertBack(b)) for a, b in numberSet]

        for j in range(len(functions)):
            startTime = time.time()
            for k in range(problems):
                functions[j](numberSet[k][0], numberSet[k][1])
            timings[j].append((n, time.time() - startTime))

        if includePython:
            startTime =time.time()
            for j in range(problems):
                # Variable Assignment is Only Fair, as the Other Algorithms Include it As Well
                temp = pythonSet[j][0] * pythonSet[j][1]

            timings[-1].append((n, time.time() - startTime))

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


    plt.title("Runtime of Various Multiplication Algorithms vs Problem Size (Base 2**12)")
    plt.xlabel("Size of Numbers (Number of Digits)")
    plt.ylabel("Time to Solve (10 Problems)")
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
def testAccuracy(start, stop, problems=10, v=False):
    assert math.log(start) / math.log(2) % 1 == 0
    assert math.log(stop) / math.log(2) % 1 == 0
    maxIter = int(math.log(stop / start) / math.log(2)) + 1
    n = start

    for i in range(maxIter):

        numberSet = [(randomBaseK(n), randomBaseK(n)) for i in range(problems)]
        for j in range(problems):
            fft = convertBack(PQ_FFT(numberSet[j][0], numberSet[j][1]))
            python = convertBack(numberSet[j][0]) * convertBack(numberSet[j][1])

            if fft != python:
                print(f"FAILED. Mismatch at n={n}. Python: {python}. FFT: {fft}")
                return False

            if v:
                print(f"MATCHED at n={n}.")

        n *= 2
    return True

def safeLog(a):
    if a == 0:
        return -1000
    return math.log(a)


if __name__ == "__main__":
    # print(randomBaseK(8))
    # print(testFFTWorks(3, v=True))
    times = timeMultiplicationFunctions([PQ_school], 64, 2**12, v=True, cutoff=2**14)
    graphTiming(times, ["School Algorithm"])
    # print(testAccuracy(2, 2**12, v=True))
    # times = timeMultiplicationFunctions([], 2048, 2**22, v=True, includePython=True)
    # graphTiming(times, ["Python Built-in"])

