import fileinput
import numpy


def bfsStep(point):
    # identify all points possibly reachable
    pointUp = (point[0]-1, point[1])
    pointDown = (point[0]+1, point[1])
    pointLeft = (point[0], point[1]-1)
    pointRight = (point[0], point[1]+1)
    points = [pointUp, pointDown, pointLeft, pointRight]
    nextPoints = []
    for p in points:
        # stay within the grid
        if p[0] < 0 or p[0] >= landscape.shape[0] or p[1] < 0 or p[1] >= landscape.shape[1]:
            continue
        # possible to move if the next point is not more than one higher than your current point
        if landscape[point]-landscape[p] <= 1 :
            # examination only usefull if there was not already a shorter path to this point
            if distance[point] < distance[p] - 1:
                nextPoints.append(p)
                distance[p] = distance[point] + 1
            if landscape[p] == ord('a'):
                print(f"found closest starting point at {p} with shortest path of only {distance[p]}")
                exit()
    return nextPoints


start = None
end = None
y = 0
landscape = []
for line in [l.strip() for l in fileinput.input()]:
    xS = line.find("S")
    xE = line.find("E")
    if xS >= 0:
        start = (y, xS)
        line = line.replace("S", "a")
    if xE >= 0:
        end = (y, xE)
        line = line.replace("E", "z")
    landscape.append([ord(x) for x in line])
    y += 1
landscape = numpy.array(landscape)
print(landscape)
distance = numpy.full(landscape.shape, numpy.iinfo(
    numpy.uint32).max, numpy.uint32)
# bfs
distance[end] = 0
nextPoint = end
search = []
while nextPoint != None:
    search += bfsStep(nextPoint)
    print(search)
    nextPoint = search.pop(0)

