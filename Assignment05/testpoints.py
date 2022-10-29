import random

def createProblem(n):
  return [[100 * random.random(), 100 * random.random()] for _ in range(n)]

