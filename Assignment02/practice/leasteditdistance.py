import numpy as np

def ledHelper(string1, string2, i1, i2):
    if i1 <= 0:
        return i2
    if i2 <= 0:
        return i1

    return min(ledHelper(string1, string2, i1 - 1, i2),
               ledHelper(string1, string2, i1, i2 - 1),
               ledHelper(string1, string2, i1 -1, i2 - 1)) + string1[i1] == string2[i2]


def led(string1, string2):
    return ledHelper(string1, string2, len(string1), len(string2))


def ledDynamic(string1, string2):
    results = np.array(np.zeros((len(string1), len(string2))))
    for i in range(1, len(results)):
        for j in range(1, (len(results[i])):
            results[i][j] = min(min(results[i - 1][j], results[i][j - 1]), results[i - 1][j - 1]) + string1[i] == string2[j]

    return results[len(string1) - 1][len(string2) - 1], results


def ledTraceback(string1, string2, results):
    solution = []
    i = len(results) - 1
    j = len(results) - 1
    while i > 0 and j > 0:
        if string1[i] == string2[j]:
            i -= 1
            j -= 1
        else:
            if results[i][j] == results[i - 1][j - 1] + 1:
                solution.append([string1[i], string2[j]])
                i -= 1
                j -= 1
            elif results[i][j] == results[i - 1][j] + 1:
                solution.append(string1[i])
                i -= 1
            elif results[i][j] == results[i][j - 1] + 1:
                solution.append(string2[j])
                j -= 1

    return solution



