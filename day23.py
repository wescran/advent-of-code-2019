from pathlib import Path
from collections import defaultdict,deque
from netcode import intcode
from itertools import chain
from copy import copy

inputFile = Path('inputs/23.txt').read_text().rstrip().split(",")

data = [int(_) for _ in inputFile]

network = []
packets = {}
#mem = {}
for i in range(50):
    network.append(intcode(i,data.copy(),0,0))
    packets[i] = deque([i])
    #mem[i] = (data.copy(),0,0)
packets[255] = deque()
print(packets)
running = True
seen = set()
while running:
    idle_count = 0
    for j,vm in enumerate(network):
        packets, idle = vm(packets)
        if idle:
            idle_count += 1
        else:
            idle_count = 0
    print(packets[255])
    if idle_count == 50:
        x = packets[255].popleft()
        y = packets[255].popleft()
        if y in seen:
            special_packet = y
            running = False
            break
        seen.add(y)
        packets[0].extend((x,y))
        
print(special_packet)
