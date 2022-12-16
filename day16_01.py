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


def dfs(valvesOpened: set[str], valves: dict[str,Valve], v : str, time: int) -> int:
    if v not in valvesOpened:
        valvesOpened.add(v)
        totalMaxPreasure = 0
        rp = 0
        nextValve = ""
        for k, d in valves[v].dists.items():
            tNew = time + d + 1
            releaseNow = (30 - tNew) * valves[k].flow
            releaseLater = dfs(valvesOpened,valves,k,tNew)
            if releaseNow + releaseLater > totalMaxPreasure:
                totalMaxPreasure =  releaseNow + releaseLater
                rp = releaseNow
                nextValve = k
        print((nextValve,time,rp,totalMaxPreasure))
        return totalMaxPreasure
    else:
        return 0

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

valves:dict[str,Valve] = {}
for line in [l.strip() for l in fileinput.input()]:
    valveStr, tunnelsStr = line.split(";")
    name = valveStr[6:8]
    flow = int(valveStr[23:])
    tunels = [t.strip() for t in tunnelsStr[23:].split(',')]
    valves[name] = Valve(name, flow, tunels)
    print(f"{name}, {flow}, {tunels}")
print(valves)
for k, v in valves.items():
    v.dists= findShortesPaths(valves,k)
    print(v.dists)

openedValves: set[str] = set()
result = dfs(openedValves,valves,"AA",0)
print(result)
s = set(valves.keys())
print(s)
print(dfs2(s,valves,"AA",0))
# open valve after n minutes, total released preasure after 30 minutes
#nextStep = ("AA", 0, 0)
#totalRelease = 0
#while nextStep[1] < 30:
#    dists = valves.get(nextStep[0]).dists
#    step = (nextStep[0],30,0)
#    for k, v in valves.items():
#        time = nextStep[1] + dists[k] + 1
#        releasablePreasure = (30 - time) * v.flow
#        if k in openedValves:
#            releasablePreasure = 0 # if k not in openedValves else 0
#        if releasablePreasure > step[2]:
#            step = (k,time,releasablePreasure)
#        print(f"{k},{time},{releasablePreasure}")
#    nextStep=step
#    openedValves.add(nextStep[0])
#    totalRelease+=nextStep[2]
#    print(f"open Valve {nextStep[0]} after {nextStep[1]} minutes. Total Release {nextStep[2]}")
#    print(openedValves)
#print(totalRelease)

