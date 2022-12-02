import copy
import math
import random


def makeExp(n):
    # n variables (use 0 ... n-1 for variables, and n .. 2n-1 for their negation
    # we always generate 4.3 * n clauses because for some reason, this ratio
    # generates the hardest problems!
    return [[random.randint(0, 2 * n - 1) for _ in range(3)] for _ in range(int(4.3 * n))]


def printSolution(exp, values, solution):
    variableValues = values + [not values[i] for i in range(len(values))]
    print("Solution is " + (" True " if solution else "False"))
    if solution:
        print("Variables = " + ''.join(["T " if values[i] else "F " for i in range(len(values))]))
        print("Clauses ")
        for clause in exp:
            print('(' + ''.join(["T " if variableValues[var] else "F " for var in clause]) + ')')


def evalExp(exp, values):
    # append the negated variables at the end
    variableValues = values + [not values[i] for i in range(len(values))]
    solution = True
    for j in range(len(exp)):
        solution = solution and evalClause(exp[j], variableValues)
        # if not solution: #short circuit evaluation
        #     break
    return solution


def evalExp1(exp, values):
    # append the negated variables at the end
    variableValues = values + [not values[i] for i in range(len(values))]
    solution = True
    for j in range(len(exp)):
        solution = solution and evalClause(exp[j], variableValues)
        if not solution:  # short circuit evaluation
            break
    return solution


def evalExp2(exp, values):
    # append the negated variables at the end
    variableValues = values
    solution = True
    for j in range(len(exp)):
        solution = solution and evalClause(exp[j], variableValues)
        if not solution:  # short circuit evaluation
            break
    return solution


def evalClause(clause, variableValues):
    return variableValues[clause[0]] or variableValues[clause[1]] or variableValues[clause[2]]


def algorithm0(exp, n, values=[]):
    # modified to return both the solution (true or false) and the variable assignments
    if n == 0:
        return (evalExp(exp, values), values)
    # Early termination strategy
    # check if the partial assignment leads to any false clauses
    (solT, valuesT) = algorithm0(exp, n - 1, [True] + values)
    # if solT: short circuit evaluation
    #     return (solT, valuesT)
    (solF, valuesF) = algorithm0(exp, n - 1, [False] + values)
    if solT:
        return (solT, valuesT)
    else:
        return (solF, valuesF)


def algorithm1(exp, n, values=[]):
    # modified to return both the solution (true or false) and the variable assignments
    if n == 0:
        return (evalExp1(exp, values), values)
    # Early termination strategy
    # check if the partial assignment leads to any false clauses
    (solT, valuesT) = algorithm1(exp, n - 1, [True] + values)
    # if solT: short circuit evaluation
    #     return (solT, valuesT)
    (solF, valuesF) = algorithm1(exp, n - 1, [False] + values)
    if solT:
        return (solT, valuesT)
    else:
        return (solF, valuesF)


def algorithm2(exp, n, values=[]):
    # modified to return both the solution (true or false) and the variable assignments
    if n == 0:
        return (evalExp1(exp, values), values)
    # Early termination strategy
    # check if the partial assignment leads to any false clauses
    (solT, valuesT) = algorithm2(exp, n - 1, [True] + values)
    if solT:  # short circuit evaluation
        return (solT, valuesT)
    (solF, valuesF) = algorithm2(exp, n - 1, [False] + values)
    if solT:
        return (solT, valuesT)
    else:
        return (solF, valuesF)


def algorithm3(exp, n):
    dict = [[] for i in range(n)]
    for i in range(len(exp)):
        maxVar = 0
        for j in range(len(exp[i])):
            testNum = exp[i][j] % n
            if testNum > maxVar:
                maxVar = testNum
        dict[maxVar].append(i)

    values = [None for i in range(2 * n)]
    return algorithm3Helper(exp, n, 0, dict, values)


def algorithm3Helper(exp, n, i, dict, values):
    # modified to return both the solution (true or false) and the variable assignments
    if i >= n:
        return (evalExp2(exp, values), values)
    # Early termination strategy
    # check if the partial assignment leads to any false clauses
    if (i > 0):
        if dict[i - 1]:
            for clause in dict[i - 1]:
                if not evalClause(exp[clause], values):
                    return False, values

    passT = copy.copy(values)
    passT[i] = True
    passT[i + n] = False

    (solT, valuesT) = algorithm3Helper(exp, n, i + 1, dict, passT)

    if solT:  # short circuit evaluation
        return (solT, valuesT)

    passF = copy.copy(values)
    passF[i] = False
    passF[i + n] = True

    (solF, valuesF) = algorithm3Helper(exp, n, i + 1, dict, passF)

    if solT:
        return (solT, valuesT)
    else:
        return (solF, valuesF)


def randomValues(n):
    values = [bool(random.getrandbits(1)) for i in range(n)]
    values += [not values[i] for i in range(n)]
    return values

def getRandomClause(exp, values):
    unsatisfied = []
    for i in range(len(exp)):
        if not evalClause(exp[i], values):
            unsatisfied.append(i)

    return exp[random.choice(unsatisfied)]

def flipRandomInClause(clause, values, n):
    index = random.choice(clause) % n
    values[index + n] = values[index]
    values[index] = not values[index]

def countUnsatisfied(exp, values):
    count = 0
    for i in range(len(exp)):
        if not evalClause(exp[i], values):
            count += 1
    return count

def getMinUnsatisfied(exp, clause, values, n):
    minCount = math.inf
    minFlip = clause[0] % n

    for i in range(len(clause)):
        var = clause[i] % n
        values[var + n] = values[var]
        values[var] = not values[var]
        count = countUnsatisfied(exp, values)
        values[var + n] = values[var]
        values[var] = not values[var]
        if count < minCount:
            minCount = minCount
            minFlip = var
    return minFlip


def walkSat(exp, n, p=0.5, maxFlips=1000):
    values = randomValues(n)
    for i in range(maxFlips):
        if evalExp2(exp, values):
            return True, values
        clause = getRandomClause(exp, values)
        if random.random() < p:
            flipRandomInClause(clause, values, n)
        else:
            minUnsatisfied = getMinUnsatisfied(exp, clause, values, n)
            values[minUnsatisfied + n] = values[minUnsatisfied]
            values[minUnsatisfied] = not values[minUnsatisfied]
    return False, []
