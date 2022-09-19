# Function to Determine if a Player Can Win a Game of Nim on Their Turn Given n Stones Remain (Recurssive)
def win_nimr(n):
	# Base Cases
	if n == 2 or n == 1:
		return true
	elif n == 0:
		return false

	return not win_nimr(n - 1) or not win_nimr(n - 2)

# Iteartive Version
def win_nim(n):
	victoryTable = [False for i in range(n + 2)]
	victoryTable[1:3] = [True, True]
	for i in range(2, n + 1):
		victoryTable[i] = not (victoryTable[i - 1] and victoryTable[i - 2])
	return victoryTable[n]