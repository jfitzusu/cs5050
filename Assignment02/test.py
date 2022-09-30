from proteinSeq import maxScoreDP, printTraceBack, traceBack
#
# # Here is some test code where we provide the solutions that DP algorithm for Assignment 2 found.
# #Problem sizes are small enough that recursive can be run
# openScore = -5
# continueScore = -1
# chars = ['A', 'T', 'C', 'G']
# import random
# #create A and B strings
# def makeProblem(seed = 11111):
#   random.seed(seed)
#   return ('_'+''.join([chars[random.randint(0, 3)] for i in range(random.randint(1, 10))]),
#           '_'+''.join([chars[random.randint(0, 3)] for i in range(random.randint(1, 10))]))
# def makeProblemSolutionSet():
#   MySolutions = []
#   for i in range(100):
#     global A, B
#     (A, B) = makeProblem(seed = i)
#     N, M = len(A)-1, len(B)-1
#     MySolutions.append(traceBack(maxScoreDP(A, B), A, B))
#   return MySolutions
# Solutions = [-18, -14, -10, -14, -6, -14, -12, -16, -12, -18, -19, -12, -13, -9, -11, -6, -8, -5, -6, -13, -14, -14, -10, -9, -20, -11, -8, -13, -4, -13, -11, -4, -11, -16, -11, -17, -12, -8, -15, -9, -14, -15, -10, -9, -11, -8, -16, -7, -11, 0, -16, -17, -11, -11, -8, -11, -7, -12, -21, -9, -13, -13, -12, -13, -11, -11, -6, -14, -12, -5, -14, -11, -11, -12, -19, -13, -6, -12, -12, -10, -10, -15, -8, -14, -6, -15, -5, -6, -11, -10, -14, -7, -9, -10, -7, -14, -10, -11, -10, -13]
# #Does my algorithm get the same answer?
#
# mySol = makeProblemSolutionSet()
#
# for i in range(len(mySol)):
#     printTraceBack(mySol[i], 3)

openScore = -5
continueScore = -1
chars = ['A', 'T', 'C', 'G']
import random


# create A and B strings
def makeProblem(seed=11111):
  random.seed(seed)
  return ('_' + ''.join([chars[random.randint(0, 3)] for i in range(random.randint(1, 10))]),
          '_' + ''.join([chars[random.randint(0, 3)] for i in range(random.randint(1, 10))]))


# here, values are made as a list[int] so that you could reproduce the same values on tests.


def makeProblemSolutionSetTrace():
  solutions = []
  for i in range(1):
    global A, B
    (A, B) = makeProblem(seed=i + 100)
    print(A, B)
    N, M = len(A) - 1, len(B) - 1
    sol = maxScoreDP(A, B)
    print(sol[-1][-1][0])
    alignment = traceBack(sol, A, B)
    printTraceBack(alignment)
    solutions.append(alignment)
  return solutions

makeProblemSolutionSetTrace()
