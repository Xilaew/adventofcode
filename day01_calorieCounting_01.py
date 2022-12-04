import fileinput

max = 0
current = 0
noElves = 0
noLines = 0
for line in fileinput.input():
    line = line.strip()
    lineval=0
    noLines += 1
    if line == "":
        noElves +=1
        print ("{noElves} Elf: {current}".format(noElves=noElves,current=current))
        if max<current:
            max=current
        current=0
    else:
        lineval = int(line)
        current += lineval
    print("l {noLines}, elf {elf}, {line}, {lineval}, current = {current}".format(noLines=noLines,elf=noElves,line=line,lineval=lineval,current=current))
noElves +=1
print ("{noLines} {noElves} Elf: {current}".format(noLines=noLines,noElves=noElves,current=current))
if max<current:
    max=current
current=0

print(max)    