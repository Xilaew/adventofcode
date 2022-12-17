import fileinput

class Valve():
    def __init__(self, name: str, flow: int, tunels: list[str]) -> None:
        self.name = name
        self.flow = flow
        self.tunels = tunels
        self.dists: dict[str, int] = {(v, 1) for v in tunels}

    def __str__(self) -> str:
        return f"Valve({self.name}, flow={self.flow}, tunels={self.tunels})"

    def __repr__(self) -> str:
        return f"Valve({self.name}, flow={self.flow}, tunels={self.tunels})"


# valves with highest flow values come first.
def filterAndSortByFlow(valves : dict[str,Valve], openValves : set[str]) -> dict[str,Valve]:
    valveSet = { k:valves[k] for k in openValves}
    valveSet = dict(sorted(valveSet.items(),key=lambda item: item[1].flow,reverse=True))
    return valveSet


def findShortesPaths(valves: dict[str, Valve], start: str) -> dict[str, int]:
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
        next = tunels.pop(0) if tunels else None
    return shortesPaths


def readInput() -> dict[str, Valve]:
    valves: dict[str, Valve] = {}
    for line in [l.strip() for l in fileinput.input()]:
        valveStr, tunnelsStr = line.split(";")
        name = valveStr[6:8]
        flow = int(valveStr[23:])
        tunels = [t.strip() for t in tunnelsStr[23:].split(',')]
        valves[name] = Valve(name, flow, tunels)
    return valves
