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
    else:
        print("inalid Direction", file=sys.stderr)
        exit(-1)
    dh = nHead[1]-tail[1]
    dv = nHead[0]-tail[0]
    # move right left
    if dh >= 2 and dv == 0:
        nTail = (tail[0], tail[1]+dh-1)
    elif dh <= -2 and dv == 0:
        nTail = (tail[0], tail[1]+dh+1)
    # move up and down
    elif dh == 0 and dv >= 2:
        nTail = (tail[0] + dv - 1, tail[1])
    elif dh == 0 and dv <= -2:
        nTail = (tail[0] + dv + 1, tail[1])
    # move diagonal
    elif dh >= 2 and abs(dv) == 1:
        nTail = (tail[0]+dv, tail[1]+dh-1)
    elif dh <= -2 and abs(dv) == 1:
        nTail = (tail[0]+dv, tail[1]+dh+1)
    # move diagonal
    elif abs(dh) == 1 and dv >= 2:
        nTail = (tail[0] + dv - 1, tail[1]+dh)
    elif abs(dh) == 1 and dv <= -2:
        nTail = (tail[0] + dv + 1, tail[1]+dh)
    elif abs(dh)<=1 and abs(dv)<=1:
        nTail=tail
    else:
        print("ERROR: case not considered", file=sys.stderr)
        exit(-1)
    return (nHead,nTail)


placesVisitedByTail = set()
head=(0,0)
tail=(0,0)
placesVisitedByTail.add(tail)
for line in fileinput.input():
    direction, lenth = [s.strip() for s in line.split(" ")]
    for i in range(0, int(lenth)):
        head, tail = move(direction, head, tail)
        placesVisitedByTail.add(tail)
print(placesVisitedByTail)
print(placesVisitedByTail.__len__())