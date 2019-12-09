from pathlib import Path
from collections import defaultdict
inputFile = Path("inputs/input-08-01.txt")
data = (int(i) for i in inputFile.read_text().rstrip())
'''
# Part 1
layers = {}
layerNum = 1
running = True
while running:
    zeroCount, oneCount, twoCount = 0,0,0
    for i in range(6*25):
        try:
            digit = next(data)
        except StopIteration:
            running = False
            break
        if digit == 0:
            zeroCount += 1
        elif digit == 1:
            oneCount += 1
        elif digit == 2:
            twoCount += 1
    if running:
        layers[layerNum] = (zeroCount,oneCount,twoCount)
        layerNum += 1
minZero = min(layers, key=lambda key: layers[key][0])
print(layers[minZero][1]*layers[minZero][2])
'''
# Part 2
layers = []
for _ in range(100):
    layer = []
    for y in range(6):
        row = []
        for x in range(25):
            row.append(next(data))
        layer.append(row)
    layers.append(layer)

image = []
for i in range(6):
    image.append(["*"]*25)
for layer in layers:
    for r in range(6):
        for c in range(25):
            if (layer[r][c] == 0 or layer[r][c] == 1) and image[r][c] == "*":
                image[r][c] = layer[r][c] if layer[r][c] == 1 else " " 

for row in image:
    print(*row)
