import math
import random
import time
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np


'''
Function Which Recursively Determines the Maximum Value of Objects That Can be Fit Into To Knapsacks
K1: Capacity of Knapsack1
K2: Capacity of Knapsack2
objectsLeft: Objects Left to be Considered (Starts at size(s) - 1)
S: Array Containing Object Sizes (The 0th Position is Empty)
V: Array Containing Object Values (The 0th Position is Empty)
'''
def recursiveKnapsacks(K1, K2, objectsLeft, S, V):
    # Base Cases
    if (K1 <= 0 and K2 <= 0) or objectsLeft <= 0:
        return 0

    # Simplified Problem

    max1 = 0 if S[objectsLeft] > K1 else recursiveKnapsacks(K1 - S[objectsLeft], K2, objectsLeft - 1, S, V) + V[objectsLeft]
    max2 = 0 if S[objectsLeft] > K2 else recursiveKnapsacks(K1, K2 - S[objectsLeft], objectsLeft - 1, S, V) + V[objectsLeft]

    return max(max(max1, max2), recursiveKnapsacks(K1, K2, objectsLeft - 1, S, V))


'''
Helper Function for the Above
'''
def knapsacksR(K1, K2, S, V):
    if len(S) != len(V):
        raise Exception("Error: Object Missing Value or Size Data")
    return recursiveKnapsacks(K1, K2, len(S) - 1, S, V)


'''
Function Which Recursively Determines the Maximum Value of Objects That Can be Fit Into To Knapsacks, Uses Memoizing
K1: Capacity of Knapsack1
K2: Capacity of Knapsack2
objectsLeft: Objects Left to be Considered (Starts at size(s) - 1)
S: Array Containing Object Sizes (The 0th Position is Empty)
V: Array Containing Object Values (The 0th Position is Empty)
cache: Stores Results of Previous Calls, -1 Indicates No Stored Result
'''
def recursiveMemoizingKnapsacks(K1, K2, objectsLeft, S, V, cache):
    if cache[objectsLeft][K1][K2] != -1:
        return cache[objectsLeft][K1][K2]

    # Base Cases
    if (K1 <= 0 and K2 <= 0) or objectsLeft <= 0:
        return 0

    # Simplified Problem
    max1 = 0 if S[objectsLeft] > K1 else recursiveMemoizingKnapsacks(K1 - S[objectsLeft], K2, objectsLeft - 1, S, V, cache) + V[objectsLeft]
    max2 = 0 if S[objectsLeft] > K2 else recursiveMemoizingKnapsacks(K1, K2 - S[objectsLeft], objectsLeft - 1, S, V, cache) + V[objectsLeft]

    maxVal = max(max(max1, max2), recursiveMemoizingKnapsacks(K1, K2, objectsLeft - 1, S, V, cache))

    cache[objectsLeft][K1][K2] = maxVal
    return maxVal


'''
Helper Function for the Above
'''
def knapsacksM(K1, K2, S, V):
    if len(S) != len(V):
        raise Exception("Error: Object Missing Value or Size Data")

    cache = np.array(np.zeros((len(S), int(K1) + 1, int(K2) + 1)), dtype=int)
    cache.fill(-1)

    return recursiveMemoizingKnapsacks(K1, K2, len(S) - 1, S, V, cache)


'''
Function Which Determines the Maximum Value of Objects That Can be Fit Into To Knapsacks Using Dynamic Programming
K1: Capacity of Knapsack1
K2: Capacity of Knapsack2
S: Array Containing Object Sizes (The 0th Position is Empty)
V: Array Containing Object Values (The 0th Position is Empty)
'''
def knapsacksDP(K1, K2, S, V):
    if len(S) != len(V):
        raise Exception("Error: Object Missing Value or Size Data")

    solutions = np.array(np.zeros((len(S), int(K1) + 1, int(K2) + 1)), dtype=int)

    for i in range(1, len(solutions)):
        for j in range(len(solutions[i])):
            for k in range(len(solutions[i][j])):
                max1 = 0 if S[i] > j else solutions[i - 1][j - S[i]][k] + V[i]
                max2 = 0 if S[i] > k else solutions[i - 1][j][k - S[i]] + V[i]
                solutions[i][j][k] = max(max(max1, max2), solutions[i - 1][j][k])

    return solutions[len(S) - 1][K1][K2]


'''
Generates Random Size Value Arrays for Objects
n: Number of Objects to Generate
aveSize:  Average Object Size
'''
def objectGenerator(n, aveSize):
    sizes = np.array(np.zeros(n + 1), dtype=int)
    values = np.array(np.zeros(n + 1), dtype=int)
    for i in range(1, len(sizes)):
        sizes[i] = random.randint(1, int(aveSize * 2))

        modifier = math.pow(10, random.randint(-10, 10) / 10)
        values[i] = int(sizes[i] * modifier)

    return sizes, values


'''
Tests the Timing of All the Functions over a Variety of Problem Sizes
n: The Maximum Problem Size
'''
def timing(n):
    aveSize = 4
    for n in range(1, n + 1):
        S, V = objectGenerator(n, aveSize)
        K1 = K2 = int(4 * n / 3)
        start = time.time()
        knapsacksR(K1, K2, S, V)
        end = time.time()
        print(f"For {n} Objects, the Recursive Algorithm Took {end - start} Seconds")


'''
Tests That All Functions Return the Same Value
'''
def testEqual(n):
    aveSize = 4
    for n in range(1, n + 1):
        S, V = objectGenerator(n, aveSize)
        K1 = K2 = int(4 * n / 3)
        recAns = knapsacksR(K1, K2, S, V)
        memAns = knapsacksM(K1, K2, S, V)
        dpAnsw = knapsacksDP(K1, K2, S, V)

        if recAns == memAns == dpAnsw:
            print("Answers Equal", end='')
        else:
            print("Answers Not Equal", end='')
        print(f"R:{recAns}, M:{memAns}, D:{dpAnsw}")


'''
Runs Timing Tests for Memoizing vs DP
'''
def graphTests():
    K1 = 20
    K2 = 30
    n = 11
    aveSizes = np.array([1, 5, 9, 13, 17, 21, 25, 29, 33, 37])
    timingM = np.array(np.zeros(len(aveSizes)))
    timingDP = np.array(np.zeros(len(aveSizes)))
    for i in range(len(aveSizes)):
        for j in range(20):
            S, V = objectGenerator(n, aveSizes[i])
            start = time.time()
            knapsacksM(K1, K2, S, V)
            timingM[i] += (time.time() - start) * 1000 / 20
            start = time.time()
            knapsacksDP(K1, K2, S, V)
            timingDP[i] += (time.time() - start) * 1000 / 20

    plt.plot(aveSizes, timingM, "g", label="Memoizing")
    plt.plot(aveSizes, timingDP, "r", label="Dynamic Programming")
    plt.title("Runtime of Memoizing vs Dynamic Programming Approach to the Knapsack Problem")
    plt.xlabel("Average Object Size")
    plt.ylabel("Time in Milliseconds")
    plt.yscale('log')
    plt.rcParams["figure.figsize"] = [16, 9]
    plt.legend()
    plt.show()




knapsacksDP(45, 57, [13, 14, 2, 9, 17, 16, 13, 10, 16, 12, 19, 7, 17, 5, 10, 5], [97, 13, 80, 33, 69, 91, 78, 19, 40, 13, 94, 10, 88, 43, 61, 72])
print("LMAO")



