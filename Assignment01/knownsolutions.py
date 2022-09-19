# Here is some test code where I provide the solutions that my DP algorithm found.
#Problem sizes are small enough that recursive can be run
import random

import knapsack

N = 15
K1 = 45
K2 = 57
def makeProblem(N, aveSize, seed = 7777777):
  # Size array and value array
  random.seed(seed)
  return ([random.randint(1,aveSize*2) for i in range(N+1)],
          [random.randint(1,100) for i in range(N+1)])
aveSize = 10

# (sizes, values) = makeProblem(N, aveSize)
# print(knap2(N,K1,K2))

def makeProblemSet(N,aveSize):
  ""
  return [makeProblem(N, aveSize, seed = i) for i in range(100)]

problems = makeProblemSet(N, aveSize)

problems2 = [1]
problems2[0] = problems[0]
MySolutions = [knapsack.knapsacksR(K1,K2,sizes, [0] + values) for (sizes, values) in problems2]
Solutions = [640, 615, 583, 602, 535, 674, 852, 712, 701, 542, 682, 691, 548, 697, 680, 693, 659, 713, 748, 537, 627, 698, 690, 677, 855, 800, 555, 860, 592, 690, 679, 698, 674, 734, 738, 635, 758, 696, 660, 739, 621, 744, 864, 495, 835, 700, 730, 599, 505, 678, 729, 486, 621, 699, 497, 709, 577, 726, 683, 544, 745, 643, 842, 716, 559, 609, 575, 655, 571, 523, 556, 728, 576, 472, 589, 548, 687, 595, 732, 723, 516, 731, 624, 702, 586, 620, 537, 701, 502, 557, 545, 706, 735, 793, 694, 606, 773, 580, 795, 656]
#Does my algorithm get the same answer?

#makeProblemSolutionSet(N,aveSize)


for i in range(len(MySolutions)):
  print(f"Problem {i + 1} Solutions {'PASS' if MySolutions[i] == Solutions[i] else 'FAIL'}. {MySolutions[i]}: {Solutions[i]}")

print(problems2)