import math

import numpy as np

def parseLine(line, dots_list, facets_list):
    arr = line.split()
    if len(arr) > 0:
        if arr[0] == 'v':
            dots_list.append(list(np.float_(arr[1:])))
        elif arr[0] == 'f':
            facets_list.append(list(map(lambda i: i - 1, list(np.int_(arr[1:])))))

def readFile(filename, dots_list, facets_list):
    with open(filename, "r") as f:
        for line in f.readlines():
            parseLine(line, dots_list, facets_list)


def getUnicPairs(facets):
    pairs = set()

    for i in range(np.shape(facets)[0]):
        a = str(facets[i][0])
        b = str(facets[i][1])
        c = str(facets[i][2])

        ls1 = list((a, b))
        ls1.sort()
        ls2 = list((a, c))
        ls2.sort()
        ls3 = list((b, c))
        ls3.sort()

        pairs.add(ls1[0] + " " + ls1[1])
        pairs.add(ls2[0] + " " + ls2[1])
        pairs.add(ls3[0] + " " + ls3[1])
    return pairs

def countDistance(first, second):
    deltaX = pow(first[0] - second[0], 2)
    deltaY = pow(first[1] - second[1], 2)
    deltaZ = pow(first[2] - second[2], 2)
    result = math.sqrt(deltaX + deltaY + deltaZ)
    return result

def countAllDistance(dots, facets):
    pairs = getUnicPairs(facets)
    count = 0

    for i in pairs:
        firstDot, secondDot = i.split()
        count += countDistance(dots[int(firstDot)], dots[int(secondDot)])
    return count

def getCenter(d1, d2, d3):
    a = (d1[0] + d2[0] + d3[0]) / 3
    b = (d1[1] + d2[1] + d3[1]) / 3
    c = (d1[2] + d2[2] + d3[2]) / 3
    result = list((a, b, c))
    return result

def getMassCentres(dots, facets):
    centres = []
    for i in facets:
        centres.append(getCenter(dots[i[0]], dots[i[1]], dots[i[2]]))

    minDist = 1000000
    maxDist = 0

    for i in range(len(centres)):
        for j in range(i + 1, len(centres)):
            dist = countDistance(centres[i], centres[j])
            if dist > maxDist:
                maxDist = dist
            elif dist < minDist:
                minDist = dist
    return list((minDist, maxDist))

dots_list = []
facets_list = []

if __name__ == '__main__':
    readFile("teapot.obj", dots_list, facets_list)
    dots = np.array(dots_list)
    facets = np.array(facets_list)

    print("Суммарная длина всех ребер, соединяющих центры тяжестей треугольников, "
          "образованных пересечением ребер =", countAllDistance(dots, facets))

    minAndMax = getMassCentres(dots, facets)
    print("Минимальное расстояние между вершинами тяжести треугольников =", minAndMax[0])
    print("Максимальное расстояние между вершинами тяжести треугольников =", minAndMax[1])
    #print(dots, "\n", facets)
