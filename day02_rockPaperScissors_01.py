import fileinput
# X for Rock (1Point)
# Y for Paper (2Points)
# Z for Scissors (3Points)
pointsMap = {
    # A for Rock 
    "A X" : 4, # 1 + 3(draw)
    "A Y" : 8, # 2 + 6(win)
    "A Z" : 3, # 3 + 0(loose)
    # B for Paper
    "B X" : 1, # 1 + 0(loose)
    "B Y" : 5, # 2 + 3(draw)
    "B Z" : 9, # 3 + 6(win)
    # C for Scissors
    "C X" : 7, # 1 + 6(win)
    "C Y" : 2, # 2 + 0(loose)
    "C Z" : 6  # 3 + 3(draw)
}

sum = 0
for line in fileinput.input():
    line = line.strip()
    val = pointsMap[line]
    sum += val
    print(f"{val}  {sum}" )
