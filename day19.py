from pathlib import Path
from collections import defaultdict
from intcode import intcode
from itertools import count
import copy

inputFile = Path('inputs/input-19-01.txt').read_text().rstrip().split(",")

data = [int(_) for _ in inputFile]
data.extend([0]*1000)

def run(inp):
    return next(intcode(data,inp))
beamed = 0
for y in range(50):
    for x in range(50):
        res = run([x,y])
        if res == 1:
            beamed += 1
print(beamed)

def get_width(x):
    for top in count(0):
        if run([x,top]) == 1:
            break
    if run([x,top+100]) == 0:
        return 0,0
    for bottom in count(top+100+1):
        if run([x,bottom]) == 0:
            break
    y = bottom - 100

    for width in count(1):
        if run([x+width,y]) == 0:
            break
    return width,y

def search(lo,hi):
    best = None
    while hi-lo > 1:
        x = (hi+lo) // 2
        width,y = get_width(x)
        print((x,y),width)
        if width >= 100:
            hi = x
            best = (x,y)
        else:
            lo = x
    return best

hi,lo = 10000,0
x,y = search(lo,hi)
print(x*10000+y)
