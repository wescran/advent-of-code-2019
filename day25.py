from pathlib import Path
from collections import defaultdict,deque
from interactive import intcode, get_command
from itertools import chain
from copy import copy

inputFile = Path('inputs/25.txt').read_text().rstrip().split(",")

data = [int(_) for _ in inputFile]

commands = {}
commands['north'] = [ord(_) for _ in "north\n"]
commands['south'] = [ord(_) for _ in "south\n"]
commands['east'] = [ord(_) for _ in "east\n"]
commands['west'] = [ord(_) for _ in "west\n"]
commands['inv'] = [ord(_) for _ in "inv\n"]
commands['take'] = lambda item: [ord(_) for _ in f"take {item}\n"]
commands['drop'] = lambda item: [ord(_) for _ in f"drop {item}\n"]

prog = intcode(data,commands)

while True:
    try:
        print(''.join(next(prog)))
    except StopIteration:
        break

