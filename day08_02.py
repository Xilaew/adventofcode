import fileinput
import numpy

def scenicScore(r:int,c:int,f:numpy.ndarray) ->int : 
    views=[f[r,c+1:],
    f[r,c-1::-1],
    f[r-1::-1,c],
    f[r+1:,c]]
#    print(f"{(r,c)}: {views}")
    score=1
    for v in views:
        visibleTrees = 0
        for i in range(0,v.size):
            visibleTrees=v.size
            if v[i] >= f[r,c]:
                visibleTrees=i+1
                break
        score*=visibleTrees
        print(f"{(r,c)}:{f[r,c]}:{v}:{visibleTrees}")
    print(f"{(r,c)}->{score}")
    return score

forest = []
for line in fileinput.input():
    line=line.strip()
    forest.append([int(x) for x in line])
forest=numpy.array(forest)
maxScore=0
bestPlace=None
for rowIndex in range(1,forest.shape[0]-1):
    for colIndex in range(1,forest.shape[1]-1):
        score = scenicScore(rowIndex,colIndex,forest)
        if score>maxScore:
            maxScore=score
            bestPlace=(rowIndex,colIndex)

print(f"maxScore={maxScore} , at={bestPlace}:{forest[bestPlace]}")