import random, time, math

import numpy as np

import matplotlib.pyplot as plt
from scipy import stats

from polymul import polyMulRecur3, polyMulRecur4, polyMulSimple


def evalPloop(P, V, n):
  #returns a list of P(V[i]) size n
  #returns the value of P at each of the values for x in V
  return [sum([P[i]*(V[j]**i) for i in range(n)]) for j in range(n)]


def evalP(P, V, n):
  #returns a list of P(V[i]) size n
  #print("Call size %3d input values = %s" % (n, str(V)))
  if n == 1:
    return [P[0]]
  #[P[i] for i in range(0,n, 2)]
  vSquared = [V[i]*V[i] for i in range(n//2)]
  evenSol = evalP(P[0::2], vSquared, n//2) #compute P_even at x^2
  oddSol = evalP(P[1::2], vSquared, n//2) #compute P odd at x^2
  return ([evenSol[i] + V[i] * oddSol[i] for i in range(n//2)] + #the answer for positive values
          [evenSol[i] - V[i] * oddSol[i] for i in range(n//2)])  #the answer for negative values
"""
Function to Test the Three Different Polynomial Multiplication Algorithms
start: Minimum Size of Polynomial, Must be a Power of 2
stop: Maximum Size of Polynomial, Must be a Power of 2
low: Lowest Possible Coefficient Value
high: Highest Possible Coefficient Value
problems: Number of Problems to Test Timing for Each Polynomial

Returns: Timing Table
"""
def timing(start, stop, low, high, problems=10):
    assert math.log(start) / math.log(2) % 1 == 0
    assert math.log(stop) / math.log(2) % 1 == 0
    maxIter = int(math.log(stop / start) / math.log(2)) + 1

    n = start
    timings = np.zeros((maxIter, 3))

    for i in range(maxIter):
        print(n)
        timings[i][0] = n

        # Generates 10 Random Problems
        poly = [random.uniform(low, high) for i in range(n)]
        V = [complex(math.cos(2*math.pi*i/n), math.sin(2*math.pi*i/n)) for i in range(n)]

        # Test Timing for Simply Multiplication
        startTime = time.time()
        for j in range(problems):
            evalPloop(poly, V, n)
        timings[i][1] = time.time() - startTime

        # Tests Timing for 4 Subproblem Multiplication
        startTime = time.time()
        for j in range(problems):
            evalP(poly, V, n)
        timings[i][2] = time.time() - startTime


        n *= 2

    return timings

def graphTiming(timings):
    sizes = [timings[i][0] for i in range(len(timings))]
    resSimple = [timings[i][1] for i in range(len(timings))]
    res4Prob = [timings[i][2] for i in range(len(timings))]


    slope1, intercept1, _, _, _ = stats.linregress([math.log(n) for n in sizes], [math.log(t) for t in resSimple])

    print("SIMPLE ALGORITHM: time = %.10f * n ^ %.10f" % (np.exp(intercept1), slope1))

    slope2, intercept2, _, _, _ = stats.linregress([math.log(n) if n > 0 else 0 for n in sizes], [math.log(t) for t in res4Prob])

    print("4SP ALGORITHM: time = %.10f * n ^ %.10f" % (np.exp(intercept2), slope2))



    plt.plot(sizes, resSimple, "g", label="Simple Algorithm")
    plt.plot(sizes, res4Prob, "r", label="Recursive 4 SubProblem Algorithm")

    plt.title("Runtime of Various Polynomial Multiplication Algorithms vs Polynomial Size")
    plt.xlabel("Size of Polynomials")
    plt.ylabel("Time to Solve (10 Problems)")
    plt.yscale('log')
    plt.xscale('log')
    plt.rcParams["figure.figsize"] = [16, 9]
    plt.legend()
    plt.show()





# Code Yoinked From https://gist.github.com/m0neysha/219bad4b02d2008e0154
def make_markdown_table(array):
    """ Input: Python list with rows of table as lists
               First element as header.
        Output: String to put into a .md file

    Ex Input:
        [["Name", "Age", "Height"],
         ["Jake", 20, 5'10],
         ["Mary", 21, 5'7]]
    """

    markdown = "\n" + str("| ")

    for e in array[0]:
        to_add = " " + str(e) + str(" |")
        markdown += to_add
    markdown += "\n"

    markdown += '|'
    for i in range(len(array[0])):
        markdown += str("-------------- | ")
    markdown += "\n"

    for entry in array[1:]:
        markdown += str("| ")
        for e in entry:
            to_add = str(e) + str(" | ")
            markdown += to_add
        markdown += "\n"

    return markdown + "\n"


if __name__ == "__main__":
    results = timing(32, 2 ** 14, -1, 1)
    graphTiming(results)
    print(make_markdown_table(results.transpose()))
