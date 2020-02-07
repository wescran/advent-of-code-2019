from pathlib import Path
from collections import defaultdict
from intcode import intcode
from itertools import chain

inputFile = Path('inputs/21.txt').read_text().rstrip().split(",")

data = [int(_) for _ in inputFile]

#Part 1
instructions = 'NOT A J\nNOT B T\nOR J T\nNOT C J\nOR T J\nAND D J\nWALK\n'
#Part 2
instructions = 'NOT A J\nNOT B T\nOR J T\nNOT C J\nAND H J\nOR T J\nAND D J\nRUN\n'
inputs = [ord(c) for c in instructions]

prog = intcode(data,inputs)

while True:
    try:
        num = next(prog)
    except StopIteration:
        break

print(num)
