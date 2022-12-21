from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
import fileinput

def getMaxGeodes(robotCosts: dict[str,dict[str,int]],rounds: int = 24) -> int:
    types : list[str]= ["ore","clay","obsidian","geode"]
    materials : dict[str,list[LpVariable]] = {"ore": [], "clay": [],"obsidian":[],"geode":[]}
    robots : dict[str,list[LpVariable]] = {"ore": [], "clay": [],"obsidian":[],"geode":[]}
    # Create the model
    model = LpProblem(name="geodeCrackers", sense=LpMaximize)

    for i in range(rounds):
        for m in types:
            materials[m].append(LpVariable(name=f"{m}[{i}]", lowBound=0, cat="Integer"))
            robots[m].append(LpVariable(name=f"{m}Robot[{i}]", lowBound=0, cat="Integer"))

    model += (robots["ore"][0] == 1, "one_ore_Robot_to_Kickstart_the_operation")
    for m in ["clay","obsidian","geode"]:
        model += (robots[m][0] == 0, f"no_{m}robots_at_start")

    for m in types:
        model += (materials[m][0] == 0,f"no_{m}_to_start")

    for i in range(1,rounds):
        for m in types:
            model += (materials[m][i] == materials[m][i-1] + robots[m][i-1],f"{m}[{i}]")
            model += (materials[m][i-1] + robotCosts["ore"][m] >= robots["ore"][i] * robotCosts["ore"][m] + robots["clay"][i] * robotCosts["clay"][m] + robots["obsidian"][i] * robotCosts["obsidian"][m] + robots["geode"][i] * robotCosts["geode"][m], f"{m}Consumtion[{i}]")
            model += (robots[m][i] >= robots[m][i-1],f"{m}Robot_monotony[{i}]")
        model += (robots["clay"][i]+robots["geode"][i]+robots["obsidian"][i]+robots["ore"][i] <= robots["clay"][i-1]+robots["geode"][i-1]+robots["obsidian"][i-1]+robots["ore"][i-1]+1,f"Max_1_robot_in_round_{i}")

    model += materials["geode"][23] + robots["geode"][23]
    status = model.solve()
    print(status)
    for m in types:
        if m == "obsidian":
            print(m,[f"{int(v.value()):2}" for v in materials[m]])
            print(m,[f"{int(v.value()):2}" for v in robots[m]])   
        else:
            print(m,'\t',[f"{int(v.value()):2}" for v in materials[m]])
            print(m,'\t',[f"{int(v.value()):2}" for v in robots[m]])
    return model.objective.value()

# Blueprint 3: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 19 clay. Each geode robot costs 3 ore and 10 obsidian.

def parseInput(line : str) -> tuple[int,dict[str,dict[str,int]]]:
    robotCosts = {
        "ore": {"ore":0,"clay":0,"obsidian":0,"geode":0},
        "clay": {"ore":0,"clay":0,"obsidian":0,"geode":0},
        "obsidian": {"ore":0,"clay":0,"obsidian":0,"geode":0},
        "geode": {"ore":0,"clay":0,"obsidian":0,"geode":0},
    }
    blueprint, costs = line.split(':')
    blueprintId = int(blueprint[10:])
    costs = costs.split('.').__iter__()
    for m in ["ore","clay","obsidian","geode"]:
        s = costs.__next__()
        materials = s.strip().removeprefix(f"Each {m} robot costs ").split("and")
        for mc in materials:
            amount, material = mc.strip().split(" ")
            robotCosts[m][material] = int(amount.strip())
    return (blueprintId, robotCosts)

qualityLevel = 0
for line in fileinput.input():
    blueprintId , robotCosts = parseInput(line)
    print(robotCosts)
    maxGeods = getMaxGeodes(robotCosts)
    print((blueprintId,maxGeods))
    qualityLevel += blueprintId*maxGeods
print(qualityLevel)


robotCosts = {
    "ore": {"ore":4,"clay":0,"obsidian":0,"geode":0},
    "clay": {"ore":2,"clay":0,"obsidian":0,"geode":0},
    "obsidian": {"ore":3,"clay":14,"obsidian":0,"geode":0},
    "geode": {"ore":2,"clay":0,"obsidian":7,"geode":0},
}


    
