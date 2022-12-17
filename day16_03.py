from day16 import readInput, findShortesPaths, Valve, filterAndSortByFlow

def upperBound(valves : dict[str,Valve], value, path0, d0, path1, d1, openValves: set[str]) -> int:
    upperBoundValue = 0
    posiblePositions=[ path0[-1], path1[-1] ]
    stillOpenValves = openValves.copy()
    while stillOpenValves:
        dmin=99999
        flowmax = (0,None)
        for k in stillOpenValves:
            for pos in posiblePositions:
                d = valves[pos].dists[k]
                if d < dmin:
                    dmin=d
            if valves[k].flow > flowmax[0]:
                flowmax = (valves[k].flow, valves[k])
        if d0<d1 and (d0 + dmin + 1) < totalTime:
            d0 = d0 + dmin + 1
            remainingTime = totalTime - d0
            value = remainingTime * flowmax[0]
            upperBoundValue += value
            posiblePositions.append(flowmax[1].name)
            stillOpenValves.remove(flowmax[1].name)
        elif (d1 + dmin + 1) < totalTime:
            d1 = d1 + dmin + 1
            remainingTime = totalTime - d1
            value = remainingTime * flowmax[0]
            upperBoundValue += value
            posiblePositions.append(flowmax[1].name)
            stillOpenValves.remove(flowmax[1].name)
        else:
            break
    return upperBoundValue


valves = readInput()
# add information about shortest path to all other valves to each valve
for k, v in valves.items():
    v.dists = findShortesPaths(valves, k)
    print(v.dists)
# we only care about opening those valves that acutally release preasure
allValves = set(valves.keys())
openValves : set[str] = set()
for v in allValves:
    if valves[v].flow > 0:
        openValves.add(v)
# some global information used in the algorithm
start = "AA"
totalTime = 26
globalBest = (0,[],0,[],0,set())
globalBests = [0] * totalTime
# BFS with greedy DFS lookahead
queue : list[tuple[int,list[str],int,list[str],int,set[str]]]=[]
 
# initialize Queue with first potential valves to open.
tmp_openValves = openValves.copy()
for k, v in filterAndSortByFlow(valves,openValves).items():
    d = valves[start].dists[k] + 1
    value = (totalTime - d ) * v.flow 
    tmp_openValves.remove(k)
    for ki, vi in filterAndSortByFlow(valves,tmp_openValves).items():
        di = valves[start].dists[ki] + 1
        valuei = (totalTime - di ) * vi.flow
        ov = openValves.copy()
        ov.remove(k)
        ov.remove(ki)
        e = (value+valuei,[k],d,[ki],di,ov)
        queue.append(e)

for e in queue:
    print(e)
    print(upperBound(valves,*e))

#exit(0)
while queue:
    e = queue.pop(0)
    totalValue, path0, d0, path1, d1, openValves = e
    # dont examine further if there is no chance to be the best path
    if totalValue + upperBound(valves,*e) < globalBest[0]:
        print('.',end='')
        continue
    # all Valves closed, we are done.
    if not openValves:
        if totalValue > globalBest[0]:
            globalBest = e
            print(f"FIN: {e}")
        continue
    valvesReachableFor0 = set()
    valvesReachableFor1 = set()
    for k in openValves:
        pos0 = path0[-1]
        pos1 = path1[-1]
        dk0 = valves[pos0].dists[k]
        dk1 = valves[pos1].dists[k]
        if dk0 + d0 + 1 < totalTime:
            valvesReachableFor0.add(k)
        if dk1 + d1 + 1 < totalTime:
            valvesReachableFor1.add(k)
    if not valvesReachableFor0 and not valvesReachableFor1:
        #print(f"TERM: {e}")
        if totalValue > globalBest[0]:
            globalBest = e
            print(f"*TERM: {e}")
        continue

    if valvesReachableFor0 and d0 <= d1:
        first = True
        for k, v in filterAndSortByFlow(valves,valvesReachableFor0).items():
            d = valves[path0[-1]].dists[k] + 1
            newD = d0 + d
            value = (totalTime - newD ) * v.flow
            newTotalValue = totalValue + value
            newPath = path0 + [k]
            newOpenValves = openValves.copy()
            newOpenValves.remove(k)
            e = (newTotalValue,newPath,newD,path1,d1,newOpenValves)
            if first:
                queue.insert(0,e)
                first = False
            else:
                queue.append(e)
    else:
        first = True
        for k, v in filterAndSortByFlow(valves,valvesReachableFor1).items():
            d = valves[path1[-1]].dists[k] + 1
            newD = d1 + d
            value = (totalTime - newD ) * v.flow
            newTotalValue = totalValue + value
            newPath = path1 + [k]
            newOpenValves = openValves.copy()
            newOpenValves.remove(k)
            e = (newTotalValue,path0,d0,newPath,newD,newOpenValves)
            if first:
                queue.insert(0,e)
                first = False
            else:
                queue.append(e)

