import fileinput

elfs = []
total = 0
for line in fileinput.input():
    elfs.append(set(line.strip()))
    print(line.strip())
    if elfs.__len__()==3 :
        res = set.intersection(*elfs)
        el = res.pop()
        val=0
        if(el.islower()):
            val = ord(el)-96
        elif(el.isupper()):
            val = ord(el)-64+26
        print(f"{el} -> {val}")
        total += val
        elfs.clear()
    #line = line.strip()
    #len=line.__len__()
    #div= int(len/2)
    #firstCompartment = line[:div]
    #secondCompartment = line[div:]
    #s1=set(firstCompartment)
    #s2=set(secondCompartment)
    #res=set.intersection(s1,s2)
    #el = res.pop()
    #val=0
    #if(el.islower()):
    #    val = ord(el)-96
    #elif(el.isupper()):
    #    val = ord(el)-64+26
    #print(f"{line} -> {firstCompartment} | {secondCompartment} : {el} -> {val}")
    #total += val
print(total)
