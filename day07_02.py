import fileinput
import pathlib
import anytree
import sys

class Node:
    def __init__(self, name ) -> None:
        self.name = name

class Directory(Node):
    def __init__(self, name , parent):
        self.name=name
        self.parent=parent
        parent.add(self)
        self.dirs = {}
        self.files = {}
        self.size=0

    def add(self, child):
        if isinstance(child,Directory):
            self.dirs[child.name]=child
        if isinstance(child,File):
            r = self.files[child.name]
            self.size-=r.size if r is not None else 0  
            self.files[child.name]=child
            self.size=self.size + child.size


class File(Node):
    def __init__(self, name : str, size : int, parent: Directory):
        self.name=name
        self.size=size
        self.parent=parent
        parent.add(self)


root = anytree.Node("/",parent=None,size=0,totalSize=0)
current = None

for line in fileinput.input():
    line = line.strip()
    l = [ l.strip() for l in line.split(' ') ]
    if l[0]=='$': # it is a command
        print(f"command {line}")
        if l[1]=="cd": #change directory
            #plausi check on leaving a directory
            if current is not None:
                cs = current.totalSize
                current.totalSize = 0
                for i in current.children:
                    current.totalSize += i.size + i.totalSize
                if cs!=current.totalSize:
                    print(f"this is an error in {current} size={cs}, sizecalc={current.size}",file=sys.stderr)
                    exit(-1)
            if l[2]=="/":
                current = root
            elif l[2]=="..":
                current = current.parent
            else:
                n = anytree.Node(l[2],current,size=0,totalSize=0)
                current = n
    elif l[0]=='dir': # its a directory
        print(f"directory {line}")
        #d = anytree.Node(l[1],parent=current,size=0,totalSize=0)
    else: # its a file
        print(f"file {line}")
        size=int(l[0])
        f = anytree.Node(l[1],parent=current,size=size,totalSize=0)
        for p in f.ancestors:
            p.totalSize+=size

requiredSpace=30000000-70000000+root.totalSize
delcanditate = root
for pre, fill, node in anytree.RenderTree(root):
    print(f"{node.totalSize:8d}  {node.size:8d}{pre}{node.name}")
    if node.totalSize>requiredSpace and node.totalSize<delcanditate.totalSize:
        delcanditate=node
print(f"required Space = {requiredSpace}")
print(delcanditate.totalSize)