import fileinput
import numpy

forest = []
for line in fileinput.input():
    line=line.strip()
    forest.append([int(x) for x in line])
forest=numpy.array(forest)
rowIndex,columnIndex = 0,0
s=set()
#iterate rows first
for row in forest:
    tallest=-1
    print(f"row{rowIndex},l2r:",end='')
    for columnIndex in range(0,row.size):
        v = row[columnIndex]
        if v > tallest:
            tallest=v
            s.add((rowIndex,columnIndex))
            print(f"{(rowIndex,columnIndex,v)}, ",end='')
    print()
    print(f"row{rowIndex},r2l:",end='')
    tallest=-1
    for columnIndex in range(row.size-1,0,-1):
        v = row[columnIndex]
        if v > tallest:
            tallest=v
            s.add((rowIndex,columnIndex))
            print(f"{(rowIndex,columnIndex,v)}, ",end='')
    print()
    rowIndex+=1
#iterate columns
rowIndex,columnIndex = 0,0
for col in forest.T:
    tallest=-1
    print(f"col{columnIndex},t2b:",end='')
    for rowIndex in range(0,col.size):
        v = col[rowIndex]
        if v > tallest:
            tallest=v
            s.add((rowIndex,columnIndex))
            print(f"{(rowIndex,columnIndex,v)}, ",end='')
    print()
    print(f"col{columnIndex},b2t:",end='')
    tallest=-1
    for rowIndex in range(col.size-1,0,-1):
        v = col[rowIndex]
        if v > tallest:
            tallest=v
            s.add((rowIndex,columnIndex))
            print(f"{(rowIndex,columnIndex,v)}, ",end='')
    print()
    columnIndex+=1

print(forest)
print(s)
print(s.__len__())