import fileinput


class Valve():
    def __init__(self, name: str, flow: int, tunels: list[str]) -> None:
        self.name = name
        self.flow = flow
        self.tunels = tunels
        self.dists: dict[str,int] = {(v,1) for v in tunels}

    def __str__(self) -> str:
        return f"Valve({self.name}, flow={self.flow}, tunels={self.tunels})"

    def __repr__(self) -> str:
        return f"Valve({self.name}, flow={self.flow}, tunels={self.tunels})"

def findShortesPaths(valves: dict[str,Valve], start: str) -> dict[str,int]:
    shortesPaths = {start: 0}
    tunels = []
    next = start
    while next != None:
        v = valves[next]
        for t in v.tunels:
            d = shortesPaths.get(t)
            if d == None or d > shortesPaths.get(next):
                shortesPaths[t] = shortesPaths[next] + 1
                tunels.append(t)
        next=tunels.pop(0) if tunels else None
    return shortesPaths

# returns an ordered list of valves released in a row.
# starts with a list of all still closed valves
def dfs2(closedValves : set[str], valves : dict[str,Valve], v : str, t: int) -> tuple[int,list[tuple[str,int,int]]]:
    bestPathValue = 0
    bestPath = []
    for nextValve in closedValves:
        nextClosedValves = closedValves.copy()
        nextClosedValves.remove(nextValve)
        nextTime = t + 1 + valves[v].dists[nextValve]
        nextValveRelease = ( 30 - nextTime ) * valves[nextValve].flow
        if nextValveRelease > 0:
            print((nextValve,nextTime,nextValveRelease))
            nextPathRelease, nextPath = dfs2(nextClosedValves,valves,nextValve,nextTime)
        else:
            nextPathRelease, nextPath = (0,[])
        if nextValveRelease + nextPathRelease > bestPathValue:
            bestPathValue = nextValveRelease + nextPathRelease
            bestPath = [(nextValve,nextTime,nextValveRelease)] + nextPath
    return (bestPathValue,bestPath)

def readInput() -> dict[str,Valve]:
    valves:dict[str,Valve] = {}
    for line in [l.strip() for l in fileinput.input()]:
        valveStr, tunnelsStr = line.split(";")
        name = valveStr[6:8]
        flow = int(valveStr[23:])
        tunels = [t.strip() for t in tunnelsStr[23:].split(',')]
        valves[name] = Valve(name, flow, tunels)
    return valves

def upperBound(valves : dict[str,Valve], openValves: set[str], remainingTime : int) -> int:
    # assuming elefant and you, each can open one valve after only one Tunnel
    valveSet = { k:valves[k] for k in openValves}
    valveSet = dict(sorted(valveSet.items(),key=lambda item: item[1].flow,reverse=True))
    upperBoundValue = 0
    elefant = False
    for k, v in valveSet.items():
        upperBoundValue += v.flow * remainingTime
        if elefant:
            remainingTime -= 2
            elefant = False
        else:
            elefant = True
    return upperBoundValue

def lowerBound(valves : dict[str,Valve], openValves: set[str], remainingTime : int, pos: tuple[str,str]) -> int:
    valveSet = { k:valves[k] for k in openValves}
    valveSet = dict(sorted(valveSet.items(),key=lambda item: item[1].flow,reverse=True))
    remainingTimes = (remainingTime,remainingTime)
    positions = pos
    lowerBoundValue = 0
    for k, v in valveSet.items():
        t0 = remainingTimes[0] - v.dists[positions[0]] - 1
        t1 = remainingTimes[1] - v.dists[positions[1]] - 1
        if t0 <= 0 and t1 <= 0:
            break
        if t0>t1:
            lowerBoundValue += t0*v.flow
            positions = (k,positions[1])
            remainingTimes = (t0,remainingTimes[1])
        else:
            lowerBoundValue += t1*v.flow
            positions = (positions[0],k)
            remainingTimes = (remainingTimes[0],t1)
    return lowerBoundValue


valves = readInput()
for k, v in valves.items():
    v.dists= findShortesPaths(valves,k)
totalTime = 26
globalBest : list[int] = [0] * totalTime
queue : list[tuple[int,list[str],list[str],set[str]]]=[]
allValves = set(valves.keys())
openValves : set[str] = set()
for v in allValves:
    if valves[v].flow > 0:
        openValves.add(v)
# BFS
queue.append((0,["AA"],["AA"],openValves))
while queue:
    totalValue, path1, path2, openValves = queue.pop(0)
    if len(path1) == len(path2):
        if len(path1)>=totalTime:
            continue
        if totalValue + upperBound(valves,openValves,totalTime-len(path1)-1) < globalBest[len(path1)-1] + lowerBound(valves,openValves,totalTime-len(path1),(path1[-1],path2[-1])):
            print('.',end='')
            continue
        if not openValves:
            continue
        print(totalValue, path1, path2, openValves)
    if len(path1) > len(path2):
        path = path2
        pos = path2[-1]
        valve = valves.get(pos)
        if pos in openValves:
            time = totalTime - len(path)
            value = time * valve.flow
            newTotalValue = totalValue + value
            newPath1 = path1
            newPath2 = path2 + [pos]
            newOpenValves = openValves.copy()
            newOpenValves.remove(pos)
            queue.append((newTotalValue,newPath1,newPath2,newOpenValves))
            if globalBest[len(newPath2)-1] < newTotalValue:
                globalBest[len(newPath2)-1] = newTotalValue
        for newPos in valve.tunels:
            queue.append((totalValue,path1,path2+[newPos],openValves))
        if globalBest[len(path1)-1] < totalValue:
            globalBest[len(path1)-1] = totalValue
    else:
        path = path1
        pos = path1[-1]
        valve = valves.get(pos)
        if pos in openValves:
            time = totalTime - len(path)
            value = time * valve.flow
            newTotalValue = totalValue + value
            newPath1 = path1 + [pos]
            newPath2 = path2
            newOpenValves = openValves.copy()
            newOpenValves.remove(pos)
            queue.append((newTotalValue,newPath1,newPath2,newOpenValves))
            if globalBest[len(newPath1)-1] < newTotalValue:
                globalBest[len(newPath1)-1] = newTotalValue
        for newPos in valve.tunels:
            queue.append((totalValue,path1+[newPos],path2,openValves))
print(globalBest)
