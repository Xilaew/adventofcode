import fileinput
import re

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

subsets = 0
stacks = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
readingStacks = True
for line in fileinput.input():
    if readingStacks:
        if line.strip() == "":
            print(stacks)
            readingStacks=False
            continue
        itemsAtLevel = [c[1] for c in chunkstring(line,4)]
        print(itemsAtLevel)
        stackindex = 1
        for c in itemsAtLevel:
            if ord(c) in range(ord('A'),ord('Z')+1):
                stacks[stackindex].insert(0,c)
            stackindex += 1
    else:
        #moving the crane
        m = re.match('move (\d+) from (\d+) to (\d+)',line.strip())
        count, source, target = [int(d) for d in m.groups()]
        print(f"move {count} from {source} to {target}")
        for i in range(count):
            el = stacks[source].pop()
            stacks[target].append(el)
        print(stacks)
solution = ""
for i in range(1,10):
    solution += stacks[i].pop()
print(solution)