import random

import numpy as np


def generateNim(n):
    assert n % 2 == 0
    return [random.randint(0, 100) for i in range(n)]


def nimRecursive(V):
    return nimRecursiveHelper(V, 0, len(V), sum(V))


def nimRecursiveHelper(V, startIndex, size, total):
    if size <= 0:
        return 0
    if size == 1:
        return V[startIndex]

    return total - min(nimRecursiveHelper(V, startIndex + 1, size - 1, total - V[startIndex]),
                       nimRecursiveHelper(V, startIndex, size - 1, total - V[startIndex + size - 1]))


def nimMemoizing(V):
    summation = sum(V)
    cache = np.array(np.zeros((len(V), len(V) + 1, summation + 1)))
    cache.fill(-1)
    return nimMemoizingHelper(V, 0, len(V), summation, cache)


def nimMemoizingHelper(V, startIndex, size, total, cache):
    if size <= 0:
        return 0
    if size == 1:
        return V[startIndex]

    if cache[startIndex][size][total] != -1:
        return cache[startIndex][size][total]

    result = total - min(nimMemoizingHelper(V, startIndex + 1, size - 1, total - V[startIndex], cache),
                         nimMemoizingHelper(V, startIndex, size - 1, total - V[startIndex + size - 1], cache))

    cache[startIndex][size][total] = result
    return result


def nimDP(V):
    resultsTable = np.array(np.zeros((len(V), len(V))))
    for i in range(len(resultsTable)):
        resultsTable[i][0] = V[i]

    for i in range(len(resultsTable) - 2, -1, -1):
        total = V[i]
        for j in range(1, len(resultsTable[i]) - i):
            total += V[i + j]
            resultsTable[i][j] = total - min(resultsTable[i + 1][j - 1], resultsTable[i][j - 1])

    return resultsTable[0][-1]
