import fileinput

calories=list()
current=0
for line in fileinput.input():
    line = line.strip()
    lineval=0
    if line == "":
        calories.append(current)
        current=0
    else:
        lineval = int(line)
        current += lineval
calories.append(current)

print(calories)
calories.sort(reverse=True)
print(calories)
print(f"{calories[0]} + {calories[1]} + {calories[2]} = {calories[0]+calories[1]+calories[2]}")
