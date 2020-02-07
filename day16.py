from pathlib import Path
from itertools import cycle, accumulate
from copy import copy

inputFile = Path('inputs/input-16-01.txt').read_text().rstrip()
original_data = [int(i) for i in inputFile]
data = original_data.copy()
print(len(data))
print(data[:7])
#data = [int(i) for i in '80871224585914546619083218645595']
count = 0
pattern = [0,1,0,-1]
while count < 1:
    new_data = []
    for i in range(len(data)):
        new_pattern = cycle([n for n in pattern for j in range(i+1)])
        #get rid of first num
        null = next(new_pattern)
        new_data.append(abs(sum(num*pat for num,pat in zip(data,new_pattern))) % 10)
    data = new_data
    count += 1

print(''.join((str(j) for j in data[:8])))

# PART 2
skip = int(''.join((str(_) for _ in data[:7])))
new_digits = (original_data * 10000)[skip:]
for _ in range(100):
    acc = list(accumulate(reversed(new_digits), lambda a,b: (a+b) % 10))
    new_digits = list(reversed(acc))

print(''.join((str(_) for _ in new_digits[:8])))
