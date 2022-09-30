import numpy as np
def polyMult(P, Q, n):
    PQ = np.array(np.zeros(2 * n - 1))
    for i in range(n):
        for j in range(n):
            PQ[i + j] += P[i] * Q[j]
    return PQ