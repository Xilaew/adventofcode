import fileinput

overlaps = 0
for line in fileinput.input():
    line = line.strip()
    set1,set2 = line.split(',')
    l1,h1 = [int(s.strip()) for s in set1.split('-')]
#    set1 = set(range(l,h))
    l2,h2 = [int(s.strip()) for s in set2.split('-')]
#    set2 = set(range(l,h))
    overlaping = False
    if h1>=l2 and l1<=h2:
        overlaping=True
    if h2>=l1 and l2<=h1:
        overlaping=True
    if overlaping:
        overlaps += 1
    print(f"{line} {overlaping}")
print(overlaps)
    
