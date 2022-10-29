import random
from closestpoints import close, closestPair, closestPairY, closestPairMerge, closestPairMergeR
from operator import itemgetter
X = 0
Y = 1
def createProblem(n):
    return [[100 * random.random(), 100 * random.random()] for _ in range(n)]


def testEqual(algorithms, problemGenerator, times, size, v=False):
    for i in range(times):
        if v:
            print(f"{i + 1}th Test")
            print("---------------")
        problem = problemGenerator(size)
        sortedProblem = sorted(problem, key=itemgetter(X))
        results = []
        for j in range(len(algorithms)):
            results.append(algorithms[j](sortedProblem, size))

        for j in range(len(results)):
            if v:
                print(f"Algorithm {j + 1}: {results[j]}")
            if results[0] != results[j]:
                print("Algorithms Not Equal")
                return False
        if v:
            print("Algorithms Equal")
            print()

    print("Algorithms Equal Over All Tests")
    return True


if __name__ == "__main__":
  testEqual([close, closestPair, closestPairY, closestPairMerge], createProblem, 10, 2 ** 10, v=True)


