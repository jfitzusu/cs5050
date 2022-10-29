import math
from operator import itemgetter

X, Y = 0, 1


# distance function (where X = 0 and Y = 1)
def dist(pt0, pt1):
    return math.sqrt((pt0[X] - pt1[X]) ** 2 + (pt0[Y] - pt1[Y]) ** 2)


# 2 nested loop algorithm
def close(pts, n):
    best = math.inf
    for i in range(n):
        for j in range(i + 1, n):
            best = min(best, dist(pts[i], pts[j]))
    return best


def closestPair(pts, n):
    # if only two points, return the distance
    if n == 2:
        return dist(pts[0], pts[1])
    # solve each sub problem and get the min distance
    minD = min(closestPair(pts[0:n // 2], n // 2), closestPair(pts[n // 2:], n // 2))
    # find the points in the band around the mid X using minD
    xMid = (pts[n // 2 - 1][X] + pts[n // 2][X]) / 2.0
    band = [pts[i] for i in range(n) if abs(pts[i][X] - xMid) <= minD]
    return min(minD, close(band, len(band)))


# Basic recursive function. You need to fill in the missing parts
# Input pts must be sorted by X
def closestPairY(pts, n):
    # if only two points, return the distance
    if n == 2:
        return dist(pts[0], pts[1])
    # solve each sub problem and get the min distance
    minD = min(closestPairY(pts[0:n // 2], n // 2), closestPairY(pts[n // 2:], n // 2))
    # find the points in the band around the mid X using minD
    xMid = (pts[n // 2 - 1][X] + pts[n // 2][X]) / 2.0
    band = [pts[i] for i in range(n) if abs(pts[i][X] - xMid) <= minD]
    # sort by Y
    band = sorted(band, key=itemgetter(Y))
    # compare point i with i+1 to i+7 in the array to find the current shortest distance
    minBand = math.inf
    for i in range(len(band) - 1):
        upper = min(len(band), i + 7)
        for j in range(i + 1, upper):
            testDist = dist(band[i], band[j])
            if testDist < minBand:
                minBand = testDist

    # fix the return step
    return min(minD, minBand)


def closestPairMerge(pts, n):
    return closestPairMergeR(pts, n)[0]
def closestPairMergeR(pts, n):
    # if only two points, return the distance
    if n == 2:
        if pts[0][Y] > pts[1][Y]:
            pts[0], pts[1] = pts[1], pts[0]
        return dist(pts[0], pts[1]), pts

    # solve each sub problem and get the min distance
    minDFirst, firstHalf = closestPairMergeR(pts[0:n // 2], n // 2)
    minDSecond, secondHalf = closestPairMergeR(pts[n // 2:], n // 2)

    mergeSorted = [None for i in range(len(firstHalf) + len(secondHalf))]
    i0 = 0
    i1 = 0
    i2 = 0
    while i0 < len(mergeSorted):
        if i1 >= len(firstHalf):
            mergeSorted[i0] = secondHalf[i2]
            i2 += 1
        elif i2 >= len(secondHalf):
            mergeSorted[i0] = firstHalf[i1]
            i1 += 1
        elif firstHalf[i1] < secondHalf[i2]:
            mergeSorted[i0] = firstHalf[i1]
            i1 += 1
        else:
            mergeSorted[i0] = secondHalf[i2]
            i2 += 1
        i0 += 1
    minD = min(minDFirst, minDSecond)

    # find the points in the band around the mid X using minD
    xMid = (pts[n // 2 - 1][X] + pts[n // 2][X]) / 2.0
    band = [mergeSorted[i] for i in range(n) if abs(mergeSorted[i][X] - xMid) <= minD]

    minBand = math.inf
    for i in range(len(band) - 1):
        upper = min(len(band), i + 7)
        for j in range(i + 1, upper):
            testDist = dist(band[i], band[j])
            if testDist < minBand:
                minBand = testDist

    return min(minBand, minD), mergeSorted
