from pathlib import Path

inputFile = Path("inputs/input-05-01.txt")
splitFile = inputFile.read_text().split(",")
data = [int(i) for i in splitFile]
num = 0
'''
# Part 1
inputNum = 1
while num < len(data):
    inst = str(data[num])
    if len(inst) < 4:
        inst = '0'*(4-len(inst)) + inst
    
    if inst[-2:] == '03':
        data[data[num+1]] = inputNum
        num += 2
        continue
    elif inst[-2:] == '04':
        print(data[data[num+1]]) if inst[-3] == '0' else print(data[num+1])
        num += 2
        continue
    elif inst[-2:] == '99':
        break

    par1 = data[data[num+1]] if inst[-3] == '0' else data[num+1]
    par2 = data[data[num+2]] if inst[-4] == '0' else data[num+2]
    if inst[-2:] == '01':
        data[data[num+3]] = par1 + par2
    elif inst[-2:] == '02':
        data[data[num+3]] = par1 * par2
    num += 4

'''
# Part 2
inputNum = 5
while num < len(data):
    # allows for easy parsing
    inst = str(data[num])
    # make sure all instrctions are of length 4
    if len(inst) < 4:
        inst = '0'*(4-len(inst)) + inst
    # these are for opcodes that have 2 or less params    
    if inst[-2:] == '03':
        data[data[num+1]] = inputNum
        num += 2
        continue
    # opcode 04 is a bit different in that it cares what value its outputting
    elif inst[-2:] == '04':
        print(data[data[num+1]]) if inst[-3] == '0' else print(data[num+1])
        num += 2
        continue
    elif inst[-2:] == '99':
        break
    
    # this part for instructions with more than 2 params
    # params determined here if they are positional or immediate
    par1 = data[data[num+1]] if inst[-3] == '0' else data[num+1]
    par2 = data[data[num+2]] if inst[-4] == '0' else data[num+2]
    if inst[-2:] == '01':
        data[data[num+3]] = par1 + par2
    elif inst[-2:] == '02':
        data[data[num+3]] = par1 * par2
    elif inst[-2:] == '05':
        if par1 != 0:
            num = par2
            continue
        num += 3
        continue
    elif inst[-2:] == '06':
        if par1 == 0:
            num = par2
            continue
        num +=3
        continue
    elif inst[-2:] == '07':
        if par1 < par2:
            data[data[num+3]] = 1
        else:
            data[data[num+3]] = 0
    elif inst[-2:] == '08':
        if par1 == par2:
            data[data[num+3]] = 1
        else:
            data[data[num+3]] = 0
    num += 4
