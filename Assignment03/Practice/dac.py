 import numpy as np
import math
import highschool


def PQ(P, Q, n):
    assert math.log(n) / math.log(2) % 1 == 0
    if n == 1:
        return [P[0] * Q[0]]

    s = np.zeros(2 * n - 1)

    addP = np.zeros(n // 2)
    addQ = np.zeros(n // 2)
    for i in range(n // 2):
        addP[i] = P[i] + P[i + n // 2]
        addQ[i] = Q[i] + Q[i + n // 2]

    s0 = PQ(P[:n // 2], Q[:n // 2], n // 2)
    s1 = PQ(addP, addQ, n // 2)
    s2 = PQ(P[n // 2:], Q[n // 2:], n // 2)

    for i in range(n - 1):
        s[i] += s0[i]
        s[i + n // 2] += s1[i]
        s[i + n] += s2[i]

    return s



P = [1, 3, 3, 4]
Q = [4, 8, 1, 2]

print(highschool.polyMult(P, Q, 4))
print(PQ(P, Q, 4))