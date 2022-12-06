import fileinput

for line in fileinput.input():
    line = line.strip()
    print(line)
    for i in range(14,line.__len__()-14):
        s = set(line[i-14:i])
        if s.__len__()==14:
            print(i)
            break
        print(f"{s}  {s.__len__()}")