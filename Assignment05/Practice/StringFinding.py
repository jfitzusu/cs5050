def find(T, P):
	n, m = len(T), len(P)
	for i in range(0, n-m):
		found =True
		for j in range(0, m):
			found = found and T[i + j] == P[j]
			if not found:
				break
		if found:
			return i
	return -1

def find2(T, P):
	matching = 0
	for i in range(len(T) - len(P)):
		if T[i] == P[matching]
			matching += 1
		else:
			matching = 0
		if matching == len(P):
			return i
	return -1