from pathlib import Path
from itertools import combinations
from collections import defaultdict
import re

inputFile = Path("inputs/input-12-01.txt").read_text().rstrip().split("\n")
rx = r"(.{1})=(-*\d+)"
data = [(re.findall(rx,moon)[0][1],re.findall(rx,moon)[1][1],re.findall(rx,moon)[2][1]) for moon in inputFile]

def gcd(a,b):
    if b==0:
        return a
    else:
        return gcd(b,a%b)
def lcm(a,b):
    return a*b//gcd(a,b)

moons = {i:[int(c) for c in data[i]] for i in range(4)}
vel = {i:[0,0,0] for i in range(4)}
time = 0
cycles = {0:0, 1:0, 2:0}
running = True
#while time < 1000:
while running:
    time += 1
    
    # determine velocities
    pairs = combinations(range(4),2)
    for pair in pairs:
        (x1,y1,z1),(x2,y2,z2) = moons[pair[0]],moons[pair[1]]
        (vx1,vy1,vz1),(vx2,vy2,vz2) = vel[pair[0]],vel[pair[1]]
        if x1 < x2:
            vx1 = vx1 + 1
            vx2 = vx2 - 1
        elif x1 > x2:
            vx1 = vx1 - 1
            vx2 = vx2 + 1
        if y1 < y2:
            vy1 = vy1 + 1
            vy2 = vy2 - 1
        elif y1 > y2:
            vy1 = vy1 - 1
            vy2 = vy2 + 1
        if z1 < z2:
            vz1 = vz1 + 1
            vz2 = vz2 - 1
        elif z1 > z2:
            vz1 = vz1 - 1
            vz2 = vz2 + 1

        vel[pair[0]],vel[pair[1]] = [vx1,vy1,vz1],[vx2,vy2,vz2]
    moons = {i:[p + v for p,v in zip(moons[i],vel[i])] for i in range(4)}
    # part 2
    axis = 0
    for v1,v2,v3,v4 in zip(*vel.values()):
        if v1==v2==v3==v4==0:
            if cycles[axis] == 0:
                cycles[axis] = time
        axis += 1
    if all(x > 0 for x in cycles.values()):
        running = False

vals = list(cycles.values())
print(lcm(lcm(vals[0]*2,vals[1]*2), vals[2]*2))

'''
energy = 0
for i in range(4):
    energy += sum(abs(n) for n in moons[i]) * sum(abs(n) for n in vel[i])
print(energy)
'''
