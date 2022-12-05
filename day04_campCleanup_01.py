import fileinput

subsets = 0
for line in fileinput.input():
    line = line.strip()
    set1,set2 = line.split(',')
    l1,h1 = [int(s.strip()) for s in set1.split('-')]
#    set1 = set(range(l,h))
    l2,h2 = [int(s.strip()) for s in set2.split('-')]
#    set2 = set(range(l,h))
    contained = False
    if l1>=l2:
        if h1<=h2:
            # set1 is subset of set2
            contained=True
    if l1<=l2:
        if h1>=h2:
            # set1 is a superset of set2
            contained=True
    if contained:
        subsets += 1
    print(f"{line} {contained}")
print(subsets)
    
