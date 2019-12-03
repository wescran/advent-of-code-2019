from pathlib import Path

inputFile = Path("inputs/input-02-01.txt")

# Part 1
splitFile = inputFile.read_text().split(",")
data = [int(i) for i in splitFile]
data[1], data[2] = 12, 2
num = 0
while num < len(data):
    if data[num] == 1:
        data[data[num+3]] = data[data[num+1]] + data[data[num+2]]
    elif data[num] == 2:
        data[data[num+3]] = data[data[num+1]] * data[data[num+2]]
    elif data[num] == 99:
        break
    num += 4

print(data[0])

# Part 2
splitFile = inputFile.read_text().split(",")
data = [int(i) for i in splitFile]
val = 19690720
for i in range(100):
    for j in range(100):
        new_data = list(data)
        new_data[1], new_data[2] = i, j
        num = 0
        while num < len(data):
            if new_data[num] == 1:
                new_data[new_data[num+3]] = new_data[new_data[num+1]] + new_data[new_data[num+2]]
            elif new_data[num] == 2:
                new_data[new_data[num+3]] = new_data[new_data[num+1]] * new_data[new_data[num+2]]
            elif new_data[num] == 99:
                break
            num += 4
        res = new_data[0]
        if res == val:
            print(100*i+j)
            break
