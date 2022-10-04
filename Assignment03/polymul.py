import numpy as np
import math

"""
Multiplies Two Polynomials of Length n by Iterativley Multiplying Each Pair of Terms
P: Polynomial One, Represented as a 1D Array of Coefficients
Q: Polynomial Two, Represented as a 1D Array of Coefficients
n: Length of Both Polynomials

Returns: PQ, the Product of the Two Polynomials, Represented as a 1D Array of Coefficients
"""


def polyMulSimple(P, Q, n):
    assert len(P) == len(Q) == n
    PQ = np.zeros(2 * n - 1)
    for i in range(n):
        for j in range(n):
            PQ[i + j] += P[i] * Q[j]

    return PQ


"""
Multiplies Two Polynomials of Length n by Recusivley Multiplying Their Upper and Lower Halves
P: Polynomial One, Represented as a 1D Array of Coefficients
Q: Polynomial Two, Represented as a 1D Array of Coefficients
n: Length of Both Polynomials

Returns: PQ, the Product of the Two Polynomials, Represented as a 1D Array of Coefficients
"""


def polyMulRecur4(P, Q, n):
    assert len(P) == len(Q) == n
    assert math.log(n) / math.log(2) % 1 == 0

    # Base Case, Only 1 Term Remaining
    if n == 1:
        return [P[0] * Q[0]]

    s = np.zeros(2 * n - 1)

    # Four Subproblems, Each Representing the Multiplication of Half of Each Polynomial
    s0 = polyMulRecur4(P[:n // 2], Q[:n // 2], n // 2)
    s1 = polyMulRecur4(P[:n // 2], Q[n // 2:], n // 2)
    s2 = polyMulRecur4(P[n // 2:], Q[:n // 2], n // 2)
    s3 = polyMulRecur4(P[n // 2:], Q[n // 2:], n // 2)

    # Combines Results
    for i in range(n - 1):
        s[i] += s0[i]
        s[i + n // 2] += s1[i] + s2[i]
        s[i + n] += s3[i]

    return s


"""
Multiplies Two Polynomials of Length n by Recusivley Multiplying Their Parts
P: Polynomial One, Represented as a 1D Array of Coefficients
Q: Polynomial Two, Represented as a 1D Array of Coefficients
n: Length of Both Polynomials

Returns: PQ, the Product of the Two Polynomials, Represented as a 1D Array of Coefficients
"""


def polyMulRecur3(P, Q, n):
    assert len(P) == len(Q) == n
    assert math.log(n) / math.log(2) % 1 == 0

    # Base Case, Only 1 Term Remaining
    if n == 1:
        return [P[0] * Q[0]]

    s = np.zeros(2 * n - 1)

    # Utilizes Algebraic Identities to Perform P0*Q1 and P1*Q0 Simultaneously
    addP = np.zeros(n // 2)
    addQ = np.zeros(n // 2)
    for i in range(n // 2):
        addP[i] = P[i] + P[i + n // 2]
        addQ[i] = Q[i] + Q[i + n // 2]

    s0 = polyMulRecur3(P[:n // 2], Q[:n // 2], n // 2)
    s1 = polyMulRecur3(addP, addQ, n // 2)
    s2 = polyMulRecur3(P[n // 2:], Q[n // 2:], n // 2)

    # Combines Results
    for i in range(n - 1):
        s[i] += s0[i]
        s[i + n // 2] += s1[i] - s0[i] - s2[i]
        s[i + n] += s2[i]

    return s


