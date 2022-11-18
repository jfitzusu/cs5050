import copy
import math
import queue
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

"""
Generates a Dereferencable Concatenation Problem
n: Length of String to Test
numberWords: Number of Substrings to Test Against
minWord: Minimum Substring Length
maxWord: Maximum Substring Length
returns: String, Substrings
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


"""
Recursive Solution to the String/SubString Problem
S: String to Test
words: Words to Test Against
Returns: True if S is Composed of Words, False Otherwise
"""
def concatRecursive(S, words):
    dictionary = {}
    for word in words:
        dictionary[word] = True
    return concatRecursiveHelper(S, 0, dictionary)


"""
Helper Function for Above
S: String to Test
index: Starting Index of String to Consider
dictionray: O(1) Lookup Object for Valid Substrings
Returns: True if S[i:] is Composed of Words, False Otherwise
"""
def concatRecursiveHelper(S, index, dictionary):
    if index >= len(S):
        return True

    for i in range(index + 1, len(S) + 1):
        if S[index: i] in dictionary and concatRecursiveHelper(S, i, dictionary):
            return True

    return False


"""
Memoizing Solution to the String/SubString Problem
S: String to Test
words: Words to Test Against
Returns: True if S is Composed of Words, False Otherwise
"""
def concatMemoizing(S, words):
    dictionary = {}
    cache = [None for i in range(len(S))]
    for word in words:
        dictionary[word] = True
    return concatMemoizingHelper(S, 0, dictionary, cache)


"""
Helper Function for Above
S: String to Test
index: Starting Index of String to Consider
dictionray: O(1) Lookup Object for Valid Substrings
cache: Global Storage Object for Results of Previous Calls
Returns: True if S[i:] is Composed of Words, False Otherwise
"""
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


"""
DP Solution to the String/SubString Problem
S: String to Test
words: Words to Test Against
traceback: Boolean. Determines Return Value. 
Returns: True if S is Composed of Words, False Otherwise
Returns (Traceback): Array of Subsolutions
"""
def concatDP(S, words, traceback=False):
    dictionary = {}
    for word in words:
        dictionary[word] = True
    return concatDPHelper(S, dictionary, traceback)


"""
Helper Function for Above
S: String to Test
dictionary: O(1) Lookup for Valid Substrings
traceback: Boolean. Determines Return Value. 
Returns: True if S is Composed of Words, False Otherwise
Returns (Traceback): Array of Subsolutions
"""
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


"""
Traceback Function for String/Substring Problem
results: Array of Subsolutions
S: Original String
words: Original Substrings
returns: List of Substrings that Makeup S
"""
def concatTraceback(results, S, words):
    dictionary = {}
    for word in words:
        dictionary[word] = True
    return concatTracebackHelper(results, S, dictionary)


"""
Helper Function for Above
results: Array of Subsolutions
S: Original String
dictionary: O(1) Lookup for Valid Substrings
returns: List of Substrings that Makeup S
"""
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


"""
Prints Traceback for String/Substring Problem
words: List of Substrings Making up S
S: Original String
wordList: List of Valid Substrings
"""
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
Generates a Dereferencable Grid Problem of Size n
n: Size of Grid Axes
minJump: Smallest Possible Movement Value
maxJump: Largest Possible Movement Value
returns: (Grid Dimensions), (Starting Position), List of Valid Moves
"""
def generateGrid(n, minJump=-4, maxJump=4):
    moves = max(n // 10, 1)
    moveList = []
    for i in range(moves):
        move = (random.randint(minJump, maxJump), random.randint(minJump, maxJump), random.randint(minJump, maxJump))
        moveList.append(move)
    start = (random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1))
    return (n, n, n), start, moveList

"""
Memozing Solution to the Grid Problem
grid: Dimensions of Grid (n x m x l)
start: Player Starting Location in Grid
moves: List of Moves Available to Player
returns: n x m x l Sized Array of Booleans, True Representing a Reachable Cube
"""
def gridMemoizing(grid, start, moves):
    cache = np.array(np.zeros(grid))
    gridMemoizingHelper(grid, *start, moves, cache)
    return cache

"""
Helper Function for Above
grid: Dimensions of Grid (n x m x l)
x, y, z: Current x, y, z Coordinates of Player
moves: List of Moves Available to Player
cache: n x m x l Sized Array to Track Results In
Returns: Void
"""
def gridMemoizingHelper(grid, x, y, z, moves, cache):
    if x >= grid[0] or x < 0:
        return
    if y >= grid[1] or y < 0:
        return
    if z >= grid[2] or z < 0:
        return

    if cache[x][y][z]:
        return

    else:
        cache[x][y][z] = 1

    for move in moves:
        gridMemoizingHelper(grid, x + move[0], y + move[1], z + move[2], moves, cache)

"""
Dynamic Programming Solution to the Grid Problem
grid: Dimensions of Grid (n x m x l)
start: Player Starting Location in Grid
moves: List of Moves Available to Player
returns: n x m x l Sized Array of (Reachable, (From))
"""
def gridDP(grid, start, moves):
    solutions = [[[(False, (0, 0, 0)) for i in range(grid[2])] for j in range(grid[1])] for k in range(grid[0])]
    points = queue.Queue()
    solutions[start[0]][start[1]][start[2]] = (True, (-1, -1, -1))
    points.put(start)
    while not points.empty():
        currentPoint = points.get()
        for move in moves:
            newX = currentPoint[0] + move[0]
            newY = currentPoint[1] + move[1]
            newZ = currentPoint[2] + move[2]
            if newX >= grid[0] or newX < 0:
                continue
            if newY >= grid[1] or newY < 0:
                continue
            if newZ >= grid[2] or newZ < 0:
                continue
            if not solutions[newX][newY][newZ][0]:
                solutions[newX][newY][newZ] = (True, (currentPoint[0], currentPoint[1], currentPoint[2]))
                points.put((newX, newY, newZ))
    return solutions

"""
Prints the Move Order Needed to Reach a Certain Point
solutions: Array of Reachable/Unreachable Points
point: The Point to Reach
returns: Void
"""
def gridTracebackSingle(solutions, point):
    print(f"How to Get to Point {point}")
    if not solutions[point[0]][point[1]][point[2]][0]:
        print(    "Point Not Reachable")
        return
    path = []
    path.append(point)
    newX, newY, newZ = solutions[point[0]][point[1]][point[2]][1]
    while newX != -1:
        path.append((newX, newY, newZ))
        newX, newY, newZ = solutions[newX][newY][newZ][1]
    path.reverse()
    previousPoint = "Start"
    for i, point in enumerate(path):
        print(f"    Move {i}: {previousPoint} -> {point}")
        previousPoint = point


"""
Prints All Reachable Points
solutions: Array of Reachable/Unreachable Points
startPoint: The Starting Location
returns: Void
"""
def gridTracebackAll(solutions, startPoint):
    print(f"Reachable Points from {startPoint}:")
    for i in range(len(solutions)):
        for j in range(len(solutions[i])):
            for k in range(len(solutions[i][j])):
                if solutions[i][j][k][0]:
                    print(f"    {(i, j, k)}")

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
Generates a Dereferencable Knapsack Problem of Size n
n: Size of Both Knapsacks
items: Number of Items to Consider
itemMin: Minimum Item Size
itemMax: Maximum Item Size
"""
def generateKnapsack(n, items=2, itemMin=1, itemMax=10):
    W = []
    for i in range(items):
        W.append(random.randint(itemMin, itemMax))
    return (n, n, W)


"""
Recursive Solution to the Knapsack Problem
k1: Size of Knapsack1
k2: Size of Knapsack2
W: List of Items
returns: True if an Exact Fit Exists
"""
def knapsackRecursive(k1, k2, W):
    return knapsackRecursiveHelper(k1, k2, len(W) - 1, W)

"""
Helper Function for Above
k1: Remaining Capacity of Knapsack1
k2: Remaining Capacity of Knapsack2
i: Index of Item to Consider
W: List of Items
returns: True if an Exact Fit Exists
"""
def knapsackRecursiveHelper(k1, k2, i, W):
    if k1 < 0 or k2 < 0:
        return False

    if k1 == 0 and k2 == 0:
        return True

    if i < 0:
        return False

    return max(knapsackRecursiveHelper(k1 - W[i], k2, i, W), knapsackRecursiveHelper(k1, k2 - W[i], i, W),
               knapsackRecursiveHelper(k1, k2, i - 1, W))

"""
Memoizing Solution to the Knapsack Problem
k1: Size of Knapsack1
k2: Size of Knapsack2
W: List of Items
returns: True if an Exact Fit Exists
"""
def knapsackMemoizing(k1, k2, W):
    cache = np.array(np.zeros((k1 + 1, k2 + 1, len(W))), dtype=int)
    cache.fill(-1)
    return knapsackMemoizingHelper(k1, k2, len(W) - 1, W, cache)

"""
Helper Function for Above
k1: Remaining Capacity of Knapsack1
k2: Remaining Capacity of Knapsack2
i: Index of Item to Consider
W: List of Items
cache: Global Array to Track Results of Previous Calls
returns: True if an Exact Fit Exists
"""
def knapsackMemoizingHelper(k1, k2, i, W, cache):
    if k1 < 0 or k2 < 0:
        return False

    if k1 == 0 and k2 == 0:
        return True

    if i < 0:
        return False

    if cache[k1][k2][i] != -1:
        return cache[k1][k2][i]

    noTake = knapsackMemoizingHelper(k1, k2, i - 1, W, cache)
    take1 = knapsackMemoizingHelper(k1 - W[i], k2, i, W, cache)
    take2 = knapsackMemoizingHelper(k1, k2 - W[i], i, W, cache)

    sol = max(noTake, take1, take2)
    cache[k1][k2][i] = sol
    return sol

"""
Dynamic Programming Solution to the Knapsack Problem
k1: Size of Knapsack1
k2: Size of Knapsack2
W: List of Items
traceback: Controls Return Type
returns: True if an Exact Fit Exists
returns (traceback): Array of Subsolutions
"""
def knapsackDP(k1, k2, W, traceback=False):
    resultsTable = np.array(np.zeros((k1 + 1, k2 + 1, len(W))), dtype=bool)

    for i in range(len(W)):
        resultsTable[0][0][i] = True
    for i in range(len(resultsTable)):
        for j in range(len(resultsTable[i])):
            for k in range(len(W)):
                if i == 0 and k == 0:
                    break
                noTake = resultsTable[i][j][k - 1]
                take1 = False if W[k] > i else resultsTable[i - W[k]][j][k]
                take2 = False if W[k] > j else resultsTable[i][j - W[k]][k]
                resultsTable[i][j][k] = noTake or take1 or take2

    if traceback:
        return resultsTable

    return resultsTable[-1][-1][-1]


"""
Traceback for Knapsack Problem
resultsTable: Array of Subsolutions
W: Original List of Items
returns: List of Items Put Into K1, List of Items Put Into K2
"""
def knapsackTraceback(resultsTable, W):
    i = len(resultsTable) - 1
    j = len(resultsTable[i]) - 1
    k = len(resultsTable[i][j]) - 1
    items1 = []
    items2 = []
    while i >= 0 and j >= 0 and k >= 0:
        if W[k] <= i and resultsTable[i - W[k]][j][k]:
            items1.append(W[k])
            i -= W[k]
        if W[k] <= j and resultsTable[i][j - W[k]][k]:
            items2.append(W[k])
            j -= W[k]
        else:
            k -= 1
    return items1, items2


"""
Prints the Traceback of the Knapsack Problem
items1: List of Items in K1
items2: List of Items in K2
size1: Size of K1
size2: Size of K2
itemList: Original Items
"""
def printKnapsack(items1, items2, size1, size2, itemList):
    print("Possible Items:")
    print(itemList)
    print(f"Items In Knapsack 1 ({size1})")
    print(items1)
    print(f"Items in Knapsack 2 ({size2})")
    print(items2)


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
Generates a Board Problem of Size n
n: Size of Board Problem
minValue: Minimum Cash Value Per Square
maxValue: Maximum Cash Value per Square
returns: 2D Array of Cash Values
"""
def generateBoard(n, minValue=0, maxValue=25):
    return [[[random.randint(minValue, maxValue) for i in range(n)] for j in range(n)]]


"""
Recursive Solution to the Board Problem
board: 2D Array of Cash Values
returns: Maximum Achievable Cash Value
"""
def boardRecursive(board):
    if len(board) == 0:
        return 0
    assert len(board) == len(board[0])
    return max([boardRecursiveHelper(board, 0, i, 0) for i in range(len(board))])


"""
Helper Function for Above
board: 2D Array of Cash Values
x: Current X Coordinate
y: Current Y coordinate
total: Running Total of Cash Collected
returns: Maximum Achievable Cash Value
"""
def boardRecursiveHelper(board, x, y, total):
    if y >= len(board[0]) or y < 0:
        return -math.inf

    total += board[x][y]
    if x >= len(board) - 1:
        return total

    return max(boardRecursiveHelper(board, x + 1, y + 1, total), boardRecursiveHelper(board, x + 1, y - 1, total))


"""
Memoizing Solution to the Board Problem
board: 2D Array of Cash Values
returns: Maximum Achievable Cash Value
"""
def boardMemoizing(board):
    if len(board) == 0:
        return 0
    assert len(board) == len(board[0])
    cache = np.array(np.zeros((len(board), len(board[0]))))
    cache.fill(-1)
    return max([boardMemoizingHelper(board, 0, i, cache) for i in range(len(board))])


"""
Helper Function for Above
board: 2D Array of Cash Values
x: Current X Coordinate
y: Current Y coordinate
cache: Global Array Used to Track Results of Previous Calls
returns: Maximum Achievable Cash Value
"""
def boardMemoizingHelper(board, x, y, cache):
    if y >= len(board[0]) or y < 0:
        return -math.inf

    if x >= len(board) - 1:
        return board[x][y]

    if cache[x][y] != -1:
        return cache[x][y]

    maxUp = boardMemoizingHelper(board, x + 1, y + 1, cache)
    maxDown = boardMemoizingHelper(board, x + 1, y - 1, cache)
    return board[x][y] + max(maxUp, maxDown)

"""
Dynamic Programming Solution to the Board Problem
board: 2D Array of Cash Values
traceBack: Controls Return Type 
returns: Maximum Achievable Cash Value
returns (traceback): Array of Subsolutions
"""
def boardDP(board, traceBack=False):
    solArray = np.array(np.zeros((len(board), len(board[0]))))
    for i in range(len(solArray[0])):
        solArray[-1][i] = board[-1][i]

    for i in range(len(solArray) - 2, -1, -1):
        for j in range(len(solArray[0])):
            upValue = -math.inf if j >= len(solArray[0]) - 1 else solArray[i + 1][j + 1]
            downValue = -math.inf if j <= 0 else solArray[i + 1][j - 1]
            solArray[i][j] = board[i][j] + max(upValue, downValue)

    if traceBack:
        return solArray

    return max(solArray[0])


"""
Traceback for Board Problem
solArray: Array of Subsolutions
Returns: Maximum Achievable Score, List of Moves Needed to Obtain Optimal Solution
"""
def boardTraceback(solArray):
    currentX = 0
    currentY = 0
    maxScore = -math.inf
    for i in range(len(solArray)):
        if solArray[0][i] > maxScore:
            currentY = i
            maxScore = solArray[0][i]

    moves = []
    moves.append((currentX, currentY))
    while currentX < len(solArray) - 1:

        moveUp = -math.inf if currentY >= len(solArray[0]) - 1 else solArray[currentX + 1][currentY + 1]
        moveDown = -math.inf if currentY <= 0 else solArray[currentX + 1][currentY - 1]
        if moveUp > moveDown:
            currentY += 1
        else:
            currentY -= 1
        currentX += 1

        moves.append((currentX, currentY))
    return maxScore, moves

"""
Prints a Solution to the Board Problem
maxScore: Maximum Achievable Score
moves: List of Moves to Achieve maxScore
board: Original Problem
returns: Void
"""
def printBoard(maxScore, moves, board):
    cellSize = math.floor(math.log(maxScore) / math.log(10)) + 4
    print(f"Max Score: {maxScore}")
    print("Starting Board:")
    print("==============================")
    niceBoard(board, cellSize)
    trackBoard = copy.deepcopy(board)
    currentScore = 0
    for i in range(len(moves)):
        currentScore += board[moves[i][0]][moves[i][1]]
        print(f"Move {i}")
        print("==============================")
        copyBoard = copy.deepcopy(board)
        copyBoard[moves[i][0]][moves[i][1]] = f'X({currentScore})'
        trackBoard[moves[i][0]][moves[i][1]] = f'X({currentScore})'
        niceBoard(copyBoard, cellSize)

    print("Overall Path:")
    print("==============================")
    niceBoard(trackBoard, cellSize)


"""
Prints a Singular Board State
board: Board State
cellSize: Maximum Width of a Cell Value
returns: Void
"""
def niceBoard(board, cellSize):
    print("-" * ((len(board) * (cellSize + 3)) + 1))
    for j in range(len(board[0])):
        for i in range(len(board)):
            if isinstance(board[i][j], int):
                print(f"| {board[i][j]:>{cellSize}.0f} ", end='')
            else:
                print(f"| {board[i][j]:>{cellSize}s} ", end='')
        print("|")
        print("-" * ((len(board) * (cellSize + 3)) + 1))

"""
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
PROBLEM 5
-------------------------------------------------
-------------------------------------------------
-------------------------------------------------
"""


"""
Generates a Nim Problem of Size n
n: Size of Problem to Generate
returns: Ordered Array of Stone Values
"""
def generateNim(n):
    assert n % 2 == 0
    return [[random.randint(0, 100) for i in range(n)]]


"""
Recursive Solution to the Nim Problem
V: Ordered Array of Stone Values
returns: Maximum Achievable Score
"""
def nimRecursive(V):
    return nimRecursiveHelper(V, 0, len(V), sum(V))


"""
Helper Function for Above
V: Ordered Array of Stone Values
startIndex: First Stone to Consider
size: Number of Stones to Consider
total: Sum of All Stone Values
returns: Maximum Achievable Score
"""
def nimRecursiveHelper(V, startIndex, size, total):
    if size <= 0:
        return 0
    if size == 1:
        return V[startIndex]

    return total - min(nimRecursiveHelper(V, startIndex + 1, size - 1, total - V[startIndex]),
                       nimRecursiveHelper(V, startIndex, size - 1, total - V[startIndex + size - 1]))

"""
Memoizing Solution to the Nim Problem
V: Ordered Array of Stone Values
returns: Maximum Achievable Score
"""
def nimMemoizing(V):
    summation = sum(V)
    cache = np.array(np.zeros((len(V), len(V) + 1, summation + 1)))
    cache.fill(-1)
    return nimMemoizingHelper(V, 0, len(V), summation, cache)


"""
Helper Function for Above
V: Ordered Array of Stone Values
startIndex: First Stone to Consider
size: Number of Stones to Consider
total: Sum of All Stone Values
cache: Global Array Used to Store Results of Previous Calls
returns: Maximum Achievable Score
"""
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


"""
Dynamic Programming Solution to the Nim Problem
V: Ordered Array of Stone Values
traceBack: Controls Return Type
returns: Maximum Achievable Score
returns (traceback): Array of Subsolutions
"""
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


"""
Traceback for Nim Problem
results: Array of Subsolutions
returns: Ordered List of Player Moves
"""
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


"""
Prints the Progression of a Game of Nim
moves: Ordered List of Player Moves
V: Original Ordered List of Stones
"""
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
