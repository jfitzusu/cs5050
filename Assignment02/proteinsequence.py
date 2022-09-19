import math
import numpy as np

SCORE_MAP = {"A": {"A": 1, "T": -5, "C": -5, "G": -1},
             "T": {"A": -5, "T": 1, "C": -1, "G": -5},
             "C": {"A": -5, "T": -1, "C": 1, "G": -5},
             "G": {"A": -1, "T": -5, "C": -5, "G": 1}
             }

OPEN_GAP = -5

CONTINUE_GAP = -1


def maxScore(seq1, seq2, i1, i2):
    if i1 <= 0 and i2 <= 0:
        return 0

    if i1 == 0:
        return OPEN_GAP + CONTINUE_GAP * (i2 - 1)

    if i2 == 0:
        return OPEN_GAP + CONTINUE_GAP * (i1 - 1)

    return max(max(OPEN_GAP + maxScoreAGap(seq1, seq2, i1 - 1, i2),
                   OPEN_GAP + maxScoreBGap(seq1, seq2, i1, i2 - 1)),
               SCORE_MAP[seq1[i1]][seq2[i2]] + maxScore(seq1, seq2, i1 - 1, i2 - 1))


def maxScoreAGap(seq1, seq2, i1, i2):
    if i1 <= 0:
        return OPEN_GAP + CONTINUE_GAP * (i2 - 1)

    if i2 <= 0:
        return CONTINUE_GAP * i1

    return max(CONTINUE_GAP + maxScoreAGap(seq1, seq2, i1 - 1, i2),
               SCORE_MAP[seq1[i1]][seq2[i2]] + maxScore(seq1, seq2, i1 - 1, i2 - 1))


def maxScoreBGap(seq1, seq2, i1, i2):
    if i2 <= 0:
        return OPEN_GAP + CONTINUE_GAP * (i1 - 1)

    if i1 <= 0:
        return CONTINUE_GAP * i2

    return max(CONTINUE_GAP + maxScoreBGap(seq1, seq2, i1, i2 - 1),
               SCORE_MAP[seq1[i1]][seq2[i2]] + maxScore(seq1, seq2, i1 - 1, i2 - 1))


def maxScoreDP(seq1, seq2):
    resultsArray = np.array(np.zeros((len(seq1), len(seq2), 3)), dtype=int)

    for i in range(1, len(resultsArray)):
        resultsArray[i][0][0] = -5 + (i - 1) * -1
        resultsArray[i][0][1] = i * -1
        resultsArray[i][0][2] = -5 + (i - 1) * -1

    for j in range(1, len(resultsArray[i])):
        resultsArray[0][j][0] = -5 + (j - 1) * -1
        resultsArray[0][j][1] = -5 + (j - 1) * -1
        resultsArray[0][j][2] = j * -1

    for i in range(1, len(resultsArray)):
        for j in range(1, len(resultsArray[i])):
            resultsArray[i][j][2] = max(resultsArray[i][j - 1][2] + CONTINUE_GAP,
                                        resultsArray[i - 1][j - 1][0] + SCORE_MAP[seq1[i]][seq2[j]])
            resultsArray[i][j][1] = max(resultsArray[i - 1][j][1] + CONTINUE_GAP,
                                        resultsArray[i - 1][j - 1][0] + SCORE_MAP[seq1[i]][seq2[j]])
            resultsArray[i][j][0] = max(OPEN_GAP + resultsArray[i - 1][j][1],
                                        OPEN_GAP + resultsArray[i][j - 1][2],
                                        SCORE_MAP[seq1[i]][seq2[j]] + resultsArray[i - 1][j - 1][0])

    return resultsArray[len(seq1) - 1][len(seq2) - 1][0]


def traceback(results):
    
