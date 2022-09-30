def evalSimple(P, v, n):
	sol = 0
	x = 1
	for i in range(n):
		sol += P[i] * x
		x *= v
	return sol

def evaluate(P, v, n):
	if n == 1:
		return [P[0], P[0]]

	v2 = v * v
	s1 = evaluate(P[0::2], v2, n // 2)
	s2 = evaluate(P[1::2], v2, n // 2)

	return [s1[0] + v * s2[0], s1[0] - v * s2[0]]


def test():
	P = [4, 1, 6, 9, 2, 4, 11, 1]
	v = 0.34

	print(evalSimple(P, v, len(P)))
	print(evalSimple(P, -v, len(P)))
	print(evaluate(P, v, len(P)))

test()