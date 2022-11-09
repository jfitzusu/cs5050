import copy
import random

import numpy as np

"""
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
PROBLEM 1
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
"""

def generateConcat(n, numberWords=10, minWord=2, maxWord=8):
    words = []
    for i in range(numberWords):
        size = random.randint(minWord, maxWord)
        word = []
        for j in range(size):
            word.append(chr(random.randint(ord('a'), ord('z'))))
        words.append(''.join(word))

    string = []
    stringSize = 0
    while stringSize < n:
        randomWord = words[random.randint(0, numberWords - 1)]
        stringSize += len(randomWord)
        string.append(randomWord)


    isNotConcat = bool(random.randint(0, 1))

    if isNotConcat:
        string.append('Z')

    return ''.join(string), words


def concatRecursive(S, words):
    dictionary = {}
    for word in words:
        dictionary[word] = True
    return concatRecursiveHelper(S, 0, dictionary)


def concatRecursiveHelper(S, index, dictionary):
    if index >= len(S):
        return True

    for i in range(index + 1, len(S) + 1):
        if S[index: i] in dictionary and concatRecursiveHelper(S, i, dictionary):
            return True

    return False


def concatMemoizing(S, words):
    dictionary = {}
    cache = [None for i in range(len(S))]
    for word in words:
        dictionary[word] = True
    return concatMemoizingHelper(S, 0, dictionary, cache)


def concatMemoizingHelper(S, index, dictionary, cache):
    if index >= len(S):
        return True

    if cache[index] is not None:
        return cache[index]

    for i in range(index + 1, len(S) + 1):
        if S[index: i] in dictionary and concatMemoizingHelper(S, i, dictionary, cache):
            cache[index] = True
            return True

    cache[index] = False
    return False


def concatDP(S, words, traceback=False):
    dictionary = {}
    for word in words:
        dictionary[word] = True
    return concatDPHelper(S, dictionary, traceback)


def concatDPHelper(S, dictionary, traceback):
    results = [False for i in range(len(S) + 1)]
    results[0] = True
    for i in range(1, len(S) + 1):
        for j in range(i):
            if results[j] and S[j:i] in dictionary:
                results[i] = True

    if traceback:
        return results

    return results[-1]



def concatTraceback(results, S, words):
    dictionary = {}
    for word in words:
        dictionary[word] = True
    return concatTracebackHelper(results, S, dictionary)

def concatTracebackHelper(results, S, dictionary):
    i = len(results) - 1
    words = []
    while i > 0:
        for j in range(i - 1, -1, -1):
            if S[j: i] in dictionary and results[j]:
                words.append(S[j:i])
                i = j
                break
    words.reverse()
    return words



def printConcat(words, S, wordList):
    print("WORDS:")
    print(wordList)
    print("ORIGINAL STRING:")
    print(S)
    for i, word in enumerate(words):
        if i == len(words) - 1:
            print(f"{word}", end='')
        else:
            print(f"{word} | ", end='')


"""
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
PROBLEM 2
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
"""
"""
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
PROBLEM 3
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
"""
"""
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
PROBLEM 4
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
"""
"""
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
PROBLEM 5
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
"""


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


def nimDP(V, traceBack=False):
    resultsTable = np.array(np.zeros((len(V), len(V))))
    for i in range(len(resultsTable)):
        resultsTable[i][0] = V[i]

    for i in range(len(resultsTable) - 2, -1, -1):
        total = V[i]
        for j in range(1, len(resultsTable[i]) - i):
            total += V[i + j]
            resultsTable[i][j] = total - min(resultsTable[i + 1][j - 1], resultsTable[i][j - 1])

    if traceBack:
        return resultsTable

    return resultsTable[0][-1]


def nimTraceback(results):
    moves = []
    i = 0
    j = len(results) - 1

    while j > 0:
        if results[i][j - 1] < results[i + 1][j - 1]:
            moves.append(-1)
        else:
            moves.append(0)
            i += 1
        j -= 1
    moves.append(0)

    return moves


def printNim(moves, V):
    board = copy.deepcopy(V)
    print("GAME START:")
    print(board)
    playerTurn = True

    for move in moves:
        print(f"Player {1 if playerTurn else 2}: {board[move]}")
        board.pop(move)
        print()
        print(board)
        playerTurn = not playerTurn
