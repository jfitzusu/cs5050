import math

from implementations import nimDP, nimMemoizing, nimRecursive, generateNim, nimTraceback, printNim
from implementations import concatRecursive, concatMemoizing, concatDP, concatTraceback, printConcat, generateConcat
def testProblemsEqual(functions, generator, start, stop, problems, v=False):
    assert start % 2 == 0
    assert stop % 2 == 0
    assert stop > start

    iterations = math.floor(math.log(stop / start) / math.log(2)) + 1


    n = start
    for i in range(iterations):
        if v:
            print(f"Testing Problem Size {n}")

        problemSet = [generator(n) for k in range(problems)]

        for problem in problemSet:
            baseline = functions[0](*problem)
            for j in range(len(functions)):
                evaluation = functions[j](*problem)
                if v:
                    print(f"    Function {j}: {evaluation} -> {'Pass' if evaluation == baseline else 'Fail'}")

                if evaluation != baseline:
                    return False

        n *= 2

    return True

def testDP(function, problems, values, v=False):
    if v:
        print("Testing DP Algorithm:")
    for i, problem in enumerate(problems):
        evaluation = function(*problem)
        if v:
            print(f"    Expected: {values[i]}, Result: {evaluation} -> {'Pass' if evaluation == values[i] else 'Fail'}")
        if evaluation != values[i]:
            return False


def problem1():
    KNOWN_PROBLEMS = [("catcatadogpersonctdogolargecatdog", ["cat", "dog", "person", "ct", "cata", "dogo", "large"]),
                      ("ctctctctctctctctctctcta", ["cat", "dog", "person", "ct", "cata", "dogo", "large"]),
                      ("abababbbbababbabaab", ["abaab", "babba", "aab", "bba"])]
    KNOWN_SOLUTIONS = [True, False, False]
    print("----------Equality Test----------")
    testProblemsEqual([concatRecursive, concatMemoizing, concatDP], generateConcat, 8, 16, 10, True)
    print("\n\n\n\n----------DP Test----------")
    testDP(concatDP, KNOWN_PROBLEMS, KNOWN_SOLUTIONS, True)
    print("\n\n\n\n----------TraceBack Test----------")
    printConcat(concatTraceback(concatDP(*(KNOWN_PROBLEMS[0]), True), *KNOWN_PROBLEMS[0]), *KNOWN_PROBLEMS[0])

def problem5():
    KNOWN_PROBLEMS = [[2, 12, 7, 14], [32, 8, 27, 54, 2, 8, 17, 10]]
    KNOWN_SOLUTIONS = [26, 104]
    print("----------Equality Test----------")
    testProblemsEqual([nimRecursive, nimMemoizing, nimDP], generateNim, 2, 16, 1, True)
    print("\n\n\n\n----------DP Test----------")
    testDP(nimDP, KNOWN_PROBLEMS, KNOWN_SOLUTIONS, True)
    print("\n\n\n\n----------TraceBack Test----------")
    printNim(nimTraceback(nimDP(KNOWN_PROBLEMS[1], True)), KNOWN_PROBLEMS[1])

if __name__ == "__main__":
    problem1()
