from day16 import readInput, findShortesPaths, Valve


def dfs(valvesOpened: set[str], valves: dict[str, Valve], v: str, time: int) -> int:
    if v not in valvesOpened:
        newValvesOpened = valvesOpened.copy()
        newValvesOpened.add(v)
        totalMaxPreasure = 0
        rp = 0
        nextValve = ""
        for k, d in valves[v].dists.items():
            tNew = time + d + 1
            releaseNow = (30 - tNew) * valves[k].flow
            releaseLater = dfs(newValvesOpened, valves, k, tNew)
            if releaseNow + releaseLater > totalMaxPreasure:
                totalMaxPreasure = releaseNow + releaseLater
                rp = releaseNow
                nextValve = k
        print((nextValve, time, rp, totalMaxPreasure))
        return totalMaxPreasure
    else:
        return 0

# returns an ordered list of valves released in a row.
# starts with a list of all still closed valves


def dfs2(closedValves: set[str], valves: dict[str, Valve], v: str, t: int) -> tuple[int, list[tuple[str, int, int]]]:
    bestPathValue = 0
    bestPath = []
    for nextValve in closedValves:
        nextClosedValves = closedValves.copy()
        nextClosedValves.remove(nextValve)
        nextTime = t + 1 + valves[v].dists[nextValve]
        nextValveRelease = (30 - nextTime) * valves[nextValve].flow
        if nextValveRelease > 0:
            #print((nextValve, nextTime, nextValveRelease))
            nextPathRelease, nextPath = dfs2(
                nextClosedValves, valves, nextValve, nextTime)
        else:
            nextPathRelease, nextPath = (0, [])
        if nextValveRelease + nextPathRelease > bestPathValue:
            bestPathValue = nextValveRelease + nextPathRelease
            bestPath = [(nextValve, nextTime, nextValveRelease)] + nextPath
    return (bestPathValue, bestPath)


valves: dict[str, Valve] = readInput()
for k, v in valves.items():
    v.dists = findShortesPaths(valves, k)
    print(v.dists)

openedValves: set[str] = set()
result = dfs(openedValves, valves, "AA", 0)
print(result)
#s = set(valves.keys())
#print(s)
#print(dfs2(s, valves, "AA", 0))

# open valve after n minutes, total released preasure after 30 minutes
#nextStep = ("AA", 0, 0)
#totalRelease = 0
# while nextStep[1] < 30:
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
# print(totalRelease)
