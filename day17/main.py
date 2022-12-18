import fileinput


def translateRock(rock: set[tuple[int, int]], y: int = 0, x: int = 0) -> set[tuple[int, int]]:
    result = set()
    for yorig, xorig in rock:
        ncoord = (yorig + y, xorig + x)
        result.add(ncoord)
    return result


def isCollission(tunnel: set[tuple[int, int]], rock: set[tuple[int, int]]) -> bool:
    for r in rock:
        if r in tunnel:
            return True
    return False


def printTunnel(tunnel: set[tuple[int, int]], rock: set[tuple[int, int]], maxHeight: int = None):
    texts: dict[int,str] = dict()
    calcMaxHeight = 0
    for ty, tx in tunnel:
        text = texts.get(ty)
        if text == None:
            text = ['.']*9
        text[tx+1] = '#'
        texts[ty]=text
    for ry,rx in rock:
        text = texts.get(ry)
        if text == None:
            text = ['.']*9
        text[rx+1] = '@'
        texts[ry]=text
        if ry>calcMaxHeight:
            calcMaxHeight=ry
    if maxHeight == None:
        maxHeight = calcMaxHeight
    for i, text in sorted(texts.items(),reverse=True):
        if i<=maxHeight:
            print(''.join(text))



rocks: list[set[tuple[int, int]]] = [{(0, 2), (0, 3), (0, 4), (0, 5)}, {(0, 3), (1, 2), (1, 3), (1, 4), (2, 3)}, {(
    0, 2), (0, 3), (0, 4), (1, 4), (2, 4)}, {(0, 2), (1, 2), (2, 2), (3, 2)}, {(0, 2), (0, 3), (1, 2), (1, 3)}]

# floor of the tunnel
tunnel: set[tuple[int, int]] = {
    (-1, 0), (-1, 1), (-1, 2), (-1, 3), (-1, 4), (-1, 5), (-1, 6)}
# adding the walls of the tunnel
for i in range(5000):
    tunnel.add((i, -1))
    tunnel.add((i, 7))

jetstreams = fileinput.input().readline().strip()

rockCounter = 0
jetstreamindex = 0
towerHeight = 0

while rockCounter < 2022:
    print(f"rockCounter = {rockCounter}")
    # rock starts falling
    rock = translateRock(rocks[rockCounter % 5], y=towerHeight+3, x=0)
    #printTunnel(tunnel,rock)
    while True:
        # Jetstream
        jetstream = jetstreams[jetstreamindex]
        jetstreamindex = (jetstreamindex + 1) % len(jetstreams)
        #print(jetstream, end='')
        #print(rock)
        if jetstream == '<':
            x = -1
        else:
            x = +1
        tmp_rock = translateRock(rock, y=0, x=x)
        if not isCollission(tunnel, tmp_rock):
            rock = tmp_rock
        # Fall
        tmp_rock = translateRock(rock, y=-1, x=0)
        if isCollission(tunnel, tmp_rock):
            for r in rock:
                tunnel.add(r)
                if r[0] + 1 > towerHeight:
                    towerHeight = r[0] + 1
            rockCounter += 1
            break
        else:
            rock = tmp_rock
print("FINAL")
#printTunnel(tunnel,{},maxHeight=25)
print(towerHeight)
