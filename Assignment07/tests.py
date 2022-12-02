from implementations import *
import math
import time
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
"""
Generates Timing Data for Different Functions testing on Varying Problem Sizes
functions: List of Functions to Time, Each of Which Takes two Lists of Integers and Multiplies Them Together
generator: Problem generator
start: Starting Problem Size 
end: Ending Problem Size 
problems: Number of Problems to Test for Each Problem Size
v: Verbose Mode
Returns: List of List of Points, One List Per Function
"""


def timeFunctions(functions, generator, start, stop, problems=10, v=False):
    maxIter = (stop - start) // 2 + 1

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

        n += 2

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
        slope, intercept, _, _, _ = stats.linregress([(n, safeLog(k)) for n, k in timings[i]])
        print(f"{names[i]}: time = {slope:.8f} * {np.exp(slope):.8f} ^ n")

    for i in range(len(names)):
        x, y = zip(*timings[i])
        plt.plot(x, y, colors[i], label=f"{names[i]}")

    plt.title("Runtime of Various SAT Algorithms vs Problem Size")
    plt.xlabel("Problem Size (Number of Variables)")
    plt.ylabel("Time to Solve (Average)")
    plt.yscale('log')
    plt.rcParams["figure.figsize"] = [16, 9]
    plt.legend()
    plt.show()


"""
Tests That Various (SAT) Functions Return the Same Results
functions: List of Functions to Test, Each of Which Takes two Lists of Integers and Multiplies Them Together
generator: Problem generator
start: Starting Problem Size 
end: Ending Problem Size 
problems: Number of Problems to Test for Each Problem Size
v: Verbose Mode
Returns: True if Functions are Equivalent Over All Problems, False Otherwise
"""


def testEqual(functions, generator, start, stop, problems=10, v=False):
    maxIter = (stop - start) // 2 + 1

    n = start
    returnValue = True

    for i in range(maxIter):
        if v:
            print(f"Running Tests for Size n={n}")

        # Generates problems Random Problems
        problemSet = [generator(n) for i in range(problems)]

        for j in range(len(problemSet)):
            if v:
                print(f"    Problem {j}:")
            results = [None for i in range(len(functions))]
            for k in range(len(functions)):
                results[k] = functions[k](problemSet[j], n)[0]
                if results[k] != results[0]:
                    if v:
                        print(f"        Function {k}: {results[k]} -> FAIL")
                    returnValue = False
                else:
                    if v:
                        print(f"        Function {k}: {results[k]} -> Pass")
        n += 2

    return returnValue

"""
Tests an Arbitrary SAT Function vs the WalkSat Algorithm Over Various MaxFlips values
functions: Function to Test
generator: Problem generator
start: Starting Maxflips Size  
end: Ending Maxflips Size 
size: The Problem Size to Test At
problems: Number of Problems to Test for Each Maxflips Size
v: Verbose Mode
Returns: A List of Speedup vs Accuracy Points
"""
def testWalkSat(function, generator, start, stop, size=20, problems=100, v=False):
    assert math.log(start) / math.log(2) % 1 == 0
    assert math.log(stop) / math.log(2) % 1 == 0
    maxIter = int(math.log(stop / start) / math.log(2)) + 1

    n = start

    speedUps = []
    for i in range(maxIter):
        if v:
            print(f"Running Tests for MaxFlips={n}")

        # Generates problems Random Problems
        problemSet = [generator(size) for i in range(problems)]
        resultsFunction = [None for i in  range(len(problemSet))]
        resultsWalkSat = [None for i in  range(len(problemSet))]

        starTime = time.time()
        for j in range(len(problemSet)):
            resultsFunction[j] = function(problemSet[j], size)[0]
        functionTime = time.time() - starTime

        starTime = time.time()
        for j in range(len(problemSet)):
            resultsWalkSat[j] = walkSat(problemSet[j], size, 0.5, n)[0]
        walkSatTime = time.time() - starTime

        correct = 0
        for j in range(len(resultsWalkSat)):
            if resultsWalkSat[j] == resultsFunction[j]:
                correct += 1

        if v:
            print(f"    Speedup: {functionTime / walkSatTime}")
            print(f"    Accuracy: {correct / problems}")
        speedUps.append((functionTime / walkSatTime, correct / problems))


        n *= 2

    return speedUps


"""
Graphs the Results from testWalkSat
speedUps: SpeedUp vs Accuracy Data
functionName: Name of the Function That Was Tested
"""
def graphSpeedUps(speedUps, functionName):

    slope, intercept, _, _, _ = stats.linregress([(n, k) for n, k in speedUps])
    print(f"WalkSAT SpeedUp vs {functionName} = {slope:.8f} * {np.exp(slope):.8f} ^ n")

    x, y = zip(*speedUps)
    plt.plot(x, y, 'ro', label=f"Speedup vs {functionName}")

    plt.title(f"Runtime of WalkSAT Algorithm vs {functionName}")
    plt.xlabel("SpeedUP (Average)")
    plt.ylabel("Accuracy (Average)")
    plt.rcParams["figure.figsize"] = [16, 9]
    plt.legend()
    plt.show()


def safeLog(a):
    if a == 0:
        return -1000
    return math.log(a)

def problem1():
    for i in range(10):
        problem = makeExp(20)
        sol, vals = algorithm0(problem, 20)
        printSolution(problem, vals, sol)

def problem2():
    timings = timeFunctions([algorithm0], makeExp, 8, 22, 5, True)
    graphTiming(timings, ["Algorithm0"])

def problem3():
    timings = timeFunctions([algorithm1], makeExp, 8, 22, 5, True)
    graphTiming(timings, ["Algorithm1"])

def problem4():
    timings = timeFunctions([algorithm2], makeExp, 8, 22, 5, True)
    graphTiming(timings, ["Algorithm2"])

def problem6():
    testEqual([algorithm2, algorithm3], makeExp, 8, 22, 5, True)
    timings = timeFunctions([algorithm3], makeExp, 16, 38, 5, True)
    graphTiming(timings, ["Algorithm3"])

def problem7():
    timings = timeFunctions([algorithm0, algorithm1, algorithm2, algorithm3], makeExp, 14, 26, 5, True)
    graphTiming(timings, ["Algorithm0", "Algorithm1", "Algorithm2", "Algorithm3"])

def problem10():
    testEqual([algorithm3, walkSat], makeExp, 24, 24, 100, True)

def problem12():
    results = testWalkSat(algorithm3, makeExp, 2**10, 2**17, size=36, v=True)
    graphSpeedUps(results, "Algorithm3")


if __name__ == "__main__":
    # problem1()
    # problem2()
    # problem3()
    # problem4()
    # problem6()
    # problem7()
    # problem10()
    problem12()