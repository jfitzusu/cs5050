import numpy as np

def cutLog(L, values, currentVal):
    if L <= 0:
        return 0

    if currentVal <= 0:
        return 0

    maxTake = 0 if currentVal > L else cutLog(L - currentVal, values, currentVal) + values[currentVal]
    return max(maxTake, cutLog(L, values, currentVal - 1))

def cutLogDP(L, values):
    results = np.array(np.zeros(L + 1, L + 1))

    for i in range(1, len(results)):
        for j in range(1, i):
            results[i][j] = max(results[i][j - i] + values[i], results[i - 1][j])

    return results[L][L]



