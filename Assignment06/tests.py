import math

from implementations import nimDP, nimMemoizing, nimRecursive, generateNim, nimTraceback, printNim
from implementations import concatRecursive, concatMemoizing, concatDP, concatTraceback, printConcat, generateConcat
from implementations import knapsackRecursive, knapsackMemoizing, knapsackDP, knapsackTraceback, printKnapsack, generateKnapsack
from implementations import generateBoard, boardRecursive, boardMemoizing, boardDP, boardTraceback, printBoard
from implementations import generateGrid, gridMemoizing, gridDP, gridTracebackSingle, gridTracebackAll

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

def testGridsEqual(start, stop, problems, v=False):
    assert start % 2 == 0
    assert stop % 2 == 0
    assert stop > start

    iterations = math.floor(math.log(stop / start) / math.log(2)) + 1


    n = start
    for i in range(iterations):
        if v:
            print(f"Testing Problem Size {n}")

        problemSet = [generateGrid(n) for k in range(problems)]

        for p, problem in enumerate(problemSet):
            memoizing = gridMemoizing(*problem)
            dynamic = gridDP(*problem)
            match = True
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        match = match and (memoizing[i][j][k] == dynamic[i][j][k][0])
            print(f"    Problem {p}-> {'Pass' if match else 'Fail'}")

            if not match:
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

def testGridDP(problems, solutions):
    print("Testing DP Algorithm:")
    for p, problem in enumerate(problems):
        result = gridDP(*problem)
        success = True
        for i in range(len(solutions[p])):
            for j in range(len(solutions[p][i])):
                for k in range(len(solutions[p][i][j])):
                    success = success and (solutions[p][i][j][k] == result[i][j][k][0])

        print(f"    Expected: {solutions[p]}\n    Result: {result}\n    -> {'Pass' if success else 'Fail'}")



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

def problem2():
    KNOWN_PROBLEMS = [[(3, 3, 3), (0, 0, 0), [(1, 0, 0), (0, 1, 0), (0, 0, 1)]]]
    KNOWN_SOLUTIONS = [[[[True, True, True], [True, True, True], [True, True, True]], [[True, True, True], [True, True, True], [True, True, True]], [[True, True, True], [True, True, True], [True, True, True]]]]
    print("----------Equality Test----------")
    testGridsEqual(16, 32, 1, True)
    print("\n\n\n\n----------DP Test----------")
    testGridDP(KNOWN_PROBLEMS, KNOWN_SOLUTIONS)
    print("\n\n\n\n----------TraceBack Test----------")
    print(f"Grid Size: {KNOWN_PROBLEMS[0][0]}")
    print(f"Starting Point: {KNOWN_PROBLEMS[0][1]}")
    print(f"Moves: {KNOWN_PROBLEMS[0][2]}")
    gridTracebackSingle(gridDP(*KNOWN_PROBLEMS[0]), (2, 2, 2))
    gridTracebackAll(gridDP(*KNOWN_PROBLEMS[0]), (0, 0, 0))


def problem3():
    KNOWN_PROBLEMS = [[9, 11, [3, 2]], [12, 32, [5, 8]], [1, 23, [1]]]
    KNOWN_SOLUTIONS = [True, False, True]
    print("----------Equality Test----------")
    testProblemsEqual([knapsackRecursive, knapsackMemoizing, knapsackDP], generateKnapsack, 4, 8, 10, True)
    print("\n\n\n\n----------DP Test----------")
    testDP(knapsackDP, KNOWN_PROBLEMS, KNOWN_SOLUTIONS, True)
    print("\n\n\n\n----------TraceBack Test----------")
    printKnapsack(*knapsackTraceback(knapsackDP(*KNOWN_PROBLEMS[0], True), KNOWN_PROBLEMS[0][2]), *KNOWN_PROBLEMS[0])

def problem4():
    KNOWN_PROBLEMS = [[[[0, 7, 8], [12, 0, 0], [1, 1, 1]]], [[[12, 12, 12], [1, 7, 9], [52, 0, 0]]], [[[8, 5, 6], [6, 5, 8], [12, 7, 3]]]]
    KNOWN_SOLUTIONS = [20, 71, 25]
    print("----------Equality Test----------")
    testProblemsEqual([boardRecursive, boardMemoizing, boardDP], generateBoard, 4, 16, 2, True)
    print("\n\n\n\n----------DP Test----------")
    testDP(boardDP, KNOWN_PROBLEMS, KNOWN_SOLUTIONS, True)
    print("\n\n\n\n----------TraceBack Test----------")
    printBoard(*boardTraceback(boardDP(*KNOWN_PROBLEMS[1], True)), *KNOWN_PROBLEMS[1])

def problem5():
    KNOWN_PROBLEMS = [[[2, 12, 7, 14]], [[32, 8, 27, 54, 2, 8, 17, 10]]]
    KNOWN_SOLUTIONS = [26, 104]
    print("----------Equality Test----------")
    testProblemsEqual([nimRecursive, nimMemoizing, nimDP], generateNim, 2, 16, 1, True)
    print("\n\n\n\n----------DP Test----------")
    testDP(nimDP, KNOWN_PROBLEMS, KNOWN_SOLUTIONS, True)
    print("\n\n\n\n----------TraceBack Test----------")
    printNim(nimTraceback(nimDP(*KNOWN_PROBLEMS[1], True)), *KNOWN_PROBLEMS[1])

if __name__ == "__main__":
    problem2()
