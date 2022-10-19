import math
import numpy as np

def PQ_school(P, Q):
    n = len(P)
    # P[i] -- is the i'th coefficient of x^i in polynomial P
    PQ = np.zeros(2 * n)
    for i in range(n):
        for j in range(n):
            PQ[i + j] += P[i] * Q[j]
            # assume the coeficients are integers (represented as floats)
    return [int(PQ[i]) for i in range(2 * n)]


def FFT(P, V, n):
    # returns a list of P(V[i]) size n
    # print("Call size %3d input values = %s" % (n, str(V)))
    if n == 1:
        return [P[0]]
    # [P[i] for i in range(0,n, 2)]
    vSquared = [V[i] * V[i] for i in range(n // 2)]
    evenSol = FFT(P[0::2], vSquared, n // 2)  # compute P_even at x^2
    oddSol = FFT(P[1::2], vSquared, n // 2)  # compute P odd at x^2
    return ([evenSol[i] + V[i] * oddSol[i] for i in range(n // 2)] +  # the answer for positive values
            [evenSol[i] - V[i] * oddSol[i] for i in range(n // 2)])  # the answer for negative values


def PQ_FFT(P, Q):
    # returns coeficients of PQ
    n = len(P)
    m = 2 * n  # how many samples
    # slice the unit circle into m vectors so each pie is 360 / m degrees wide
    V = [complex(math.cos(2 * math.pi * i / m), math.sin(2 * math.pi * i / m)) for i in range(m)]
    # print("Starting FFT algorithm")
    Psamples = FFT(P + [0.0 for _ in range(n)], V, m)  # pad with zeros
    Qsamples = FFT(Q + [0.0 for _ in range(n)], V, m)  # pad with zeros
    PQsamples = [Psamples[i] * Qsamples[i] for i in range(m)]  # calculate PQ sample values
    # Interpolation -- fitting the polynomial
    # Use the inverse FFT with V being the complex conjugate (the img axis is flipped *-1)
    Vconj = [complex(math.cos(2 * math.pi * i / m), -1 * math.sin(2 * math.pi * i / m)) for i in range(m)]
    PQ = FFT(PQsamples, Vconj, m)
    # Clean up the result
    return [int(round(x.real) / m) for x in PQ]
