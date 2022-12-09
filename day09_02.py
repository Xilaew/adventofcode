import fileinput
import sys
from math import copysign


def move(direction, head, tail):
    if direction == "R":
        nHead = (head[0], head[1]+1)
        pass
    elif direction == "L":
        nHead = (head[0], head[1]-1)
        pass
    elif direction == "U":
        nHead = (head[0]+1, head[1])
        pass
    elif direction == "D":
        nHead = (head[0]-1, head[1])
        pass
    elif direction == "F":
        nHead = head
    else:
        print("inalid Direction", file=sys.stderr)
        exit(-1)
    dh = nHead[1]-tail[1]
    dv = nHead[0]-tail[0]
    # move right left
    nTail=tail
    if abs(dh)<=1 and abs(dv)<=1:
        nTail=tail
    elif abs(dh) == 2 or abs(dv) ==2:
        if dh == 2:
            nTail = (nTail[0], nTail[1]+dh-1)
        elif dh == -2:
            nTail = (nTail[0], nTail[1]+dh+1)
        if dv == 2:
            nTail = (nTail[0]+dv-1, nTail[1])
        elif dv == -2:
            nTail = (nTail[0]+dv+1, nTail[1])
        if abs(dh)==1:
            nTail = (nTail[0], nTail[1]+dh)
        elif abs(dv)==1:
            nTail = (nTail[0]+dv, nTail[1])
    else:
        print(f"ERROR: case not considered {(dv,dh)}", file=sys.stderr)
        exit(-1)
    return (nHead,nTail)


placesVisitedByTail = set()
knots=[(0,0)]*10
print(knots)
placesVisitedByTail.add(knots[9])
for line in fileinput.input():
    direction, lenth = [s.strip() for s in line.split(" ")]
    for i in range(0, int(lenth)):
        knots[0], knots[1] = move(direction, knots[0], knots[1])
        for n in range(1,9):
            knots[n], knots[n+1] = move("F", knots[n], knots[n+1])
        placesVisitedByTail.add(knots[9])
print(placesVisitedByTail)
print(placesVisitedByTail.__len__())