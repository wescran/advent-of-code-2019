from pathlib import Path
from collections import defaultdict,deque
from intcode import intcode
from itertools import cycle

inputFile = Path('inputs/22.txt').read_text().rstrip().split("\n")
#inputFile = Path('22-test.txt').read_text().rstrip().split("\n")

shuff = []
for line in inputFile:
    if 'increment' in line:
        term = 'INC'
        count = int(line.split(' ')[-1])
    elif 'cut' in line:
        term = 'CUT'
        count = int(line.split(' ')[-1])
    elif 'stack' in line:
        term = 'STK'
        count = None
    shuff.append((term, count))

def increment(cards,num):
    res = deque(-1 for n in range(len(cards)))
    index_count = cycle(i for i in range(len(cards)))
    index = next(index_count)
    while cards:
        res[index] = cards.popleft()
        for i in range(num):
            index = next(index_count)
    return res

def cut(cards,num):
    if num > 0:
        for i in range(num):
            cards.append(cards.popleft())
    else:
        for i in range(abs(num)):
            cards.appendleft(cards.pop())
    return cards

def stack(cards):
    cards.reverse()
    return cards

deck = deque(i for i in range(10007))
for move,n in shuff:
    if move == 'INC':
        new_deck = increment(deck,n)
    elif move == 'CUT':
        new_deck = cut(deck,n)
    elif move == 'STK':
        new_deck = stack(deck)
    deck = new_deck
#print(deck)
print(deck.index(2019))

def transform(start, step, size, moves):
    for move, n in moves:
        if move == 'STK':
            start = (start - step) % size
            step = -step % size
        elif move == 'INC':
            step = (step * pow(n, size - 2, size)) % size
        elif move == 'CUT':
            if n < 0:
                n += size

            start = (start + step * n) % size

    return start, step

def repeat(start, step, size, repetitions):
    final_step = pow(step, repetitions, size)
    final_start = (start * (1 - final_step) * pow(1 - step, size - 2, size)) % size

    return final_start, final_step

start, step, size = 0, 1, 119315717514047
repetitions = 101741582076661

start, step = transform(start, step, size, shuff)
start, step = repeat(start, step, size, repetitions)

value = (start + step * 2020) % size
print(value)
