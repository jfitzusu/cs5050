def exactFit(n, objects):
		if n <= 0:
			return n == 0

		objects.remove(0)

		return exactFit(n, objects) or (n - size, objects)

def access(array, i, j):
	if i < 0 or j < 0:
		return False
	else:
		return array[i][j]

def exactFitDynamic(n, objects):
		doesFit = [[False for i in range(n + 1)] for j in range(size(objects) + 1)]
		doesFit[0] = [True for i in range(size(objects) + 1)]
		for i in range(len(doesFit)):
			for j in range(len(doesFit[i])):
				doesFit[i][j] = access(doesFit, i - 1, j) or access(doesFit, i, j - objects[j - 1])

		return doesFit[n + 1][size(objects) + 1]
