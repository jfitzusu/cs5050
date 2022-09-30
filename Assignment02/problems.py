import time
import matplotlib.pyplot as plt
import numpy as np
from proteinSeq import maxScoreDP, traceBack, printTraceBack
from scipy import stats
import sys

DATA_FILE = "./data/1632768120472.sequences.fasta"
VALID_CHARS = ['A', 'G', 'C', 'T']

'''
Parses the FASTA Formatted Sequences from a File
file: Location of FASTA Data
returns: An Array Containing Each Sequence and Its Name as a Tuple
'''


def parseSequences(file):
    sequences = []
    readFile = open(file)
    for line in readFile:
        if line[0] == ">":
            sequences.append([line[1:], "_"])
        else:
            for char in line:
                if char in VALID_CHARS:
                    sequences[-1][1] = ''.join((sequences[-1][1], char))

    return sequences


'''
Given a List of Sequences, Formatted as Strings, Will Calculate Alignment Scores for All Possible Pairs
sequences: List of Sequences, Formatted as Strings
returns: Asymmetrical List of Sequences where [i][j] is the Alignment Table of the ith and jth Sequences
'''


def compareSequences(sequences):
    comparisonTable = [[0 for i in range(len(sequences))] for j in range(len(sequences))]

    for i in range(len(sequences)):
        for j in range(i + 1, len(sequences)):
            print(i, j)
            comparisonTable[i][j] = maxScoreDP(sequences[i], sequences[j])

    return comparisonTable


'''
Compares the Timing of Aligning Two Sequences on Successivly Increasing Intervals
seq1: First Sequence
seq2: Second Sequence
startSize: Initial Slice of Sequences to Align
factor: Step Size to Increase by Each Time
maxSize: Maximum Slice of Sequences to Align
returns: A 2D Array Containing Size/Timing Tuples
'''


def compareTiming(seq1, seq2, startSize=2 ** 8, factor=2, maxSize=-1):
    timings = []
    currentSize = startSize

    if maxSize == -1:
        maxSize = max(len(seq1), len(seq2))
    else:
        maxSize = min(maxSize, max(len(seq1), len(seq2)))

    print(maxSize)
    while currentSize < maxSize:
        print(currentSize)
        start = time.time()
        maxScoreDP(seq1[0:currentSize], seq2[0:currentSize])
        timeTaken = time.time() - start
        timings.append([currentSize, timeTaken])
        currentSize *= factor

    currentSize = maxSize
    start = time.time()
    maxScoreDP(seq1[0:currentSize], seq2[0:currentSize])
    timeTaken = time.time() - start
    timings.append([currentSize, timeTaken])

    return timings


'''
Graphs the Results of a Timings Comparison and Estimates the Equation Governing It
timings: List of Tuples Containing Size/Timing Information
returns: Prints a Graph
'''
def graphTimings(timings):
    sizes = [timings[x][0] for x in range(len(timings))]
    times = [timings[x][1] for x in range(len(timings))]

    plt.plot(sizes, times, "g", label="Dyanmic Programming Alignment Algorithm")
    plt.title("Runtime of DNA Alignment Algorithm vs Size of Sequences")
    plt.xlabel("Size of Sequence")
    plt.ylabel("Time in Seconds")
    plt.yscale('log')
    plt.rcParams["figure.figsize"] = [16, 9]
    plt.legend()
    plt.show()

    slope, intercept, _, _, _ = stats.linregress([sizes], [np.log(t) if t > 0 else 2 ** -100 for t in times])
    print(f"y = {np.exp(slope)} * {np.exp(intercept)} ^ n")


seq = parseSequences(DATA_FILE)
seqNoNames = []
for i in range(len(seq)):
    seqNoNames.append(seq[i][1])

# timings1 = compareTiming(seqNoNames[1], seqNoNames[2], startSize=2 ** 8)
# print(timings1)
# graphTimings(timings1)

# f = open("Printouts.md", "w")
# comparisons = compareSequences(seqNoNames[:2])
#
# back = traceBack(comparisons[0][])

# sys.stdout = f
# for i in range(len(comparisons)):
#     print("\n-----------------------------------------------------------\n")
#     for j in range(len(comparisons)):
#         if isinstance(comparisons[i][j], int):
#             pass
#         else:
#             trace = traceBack(comparisons[i][j], seqNoNames[i], seqNoNames[j])
#             print(f"TraceBack for {i}, {j} Alignment")
#             printTraceBack(trace, 100)



comparisons = compareSequences(seqNoNames[0:2])
traceBack = traceBack(comparisons[0][1], seqNoNames[0], seqNoNames[1])
printTraceBack(traceBack, 100)
