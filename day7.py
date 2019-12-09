from pathlib import Path
from itertools import permutations
from collections import defaultdict

inputFile = Path("inputs/input-07-01.txt")
splitFile = inputFile.read_text().split(",")
'''
# Part 1
phases = permutations(range(0,5))
outputs = []
for phase in phases:
    inputNum = 0
    for inputPhase in phase:
        data = [int(i) for i in splitFile]
        input2 = False
        num = 0
        while num < len(data):
            # allows for easy parsing
            inst = str(data[num])
            # make sure all instrctions are of length 4
            if len(inst) < 4:
                inst = '0'*(4-len(inst)) + inst
            # these are for opcodes that have 2 or less params    
            if inst[-2:] == '03':
                if not input2:
                    data[data[num+1]] = inputPhase
                    input2 = True
                else:
                    data[data[num+1]] = inputNum
                num += 2
                continue
            # opcode 04 is a bit different in that it cares what value its outputting
            elif inst[-2:] == '04':
                if inst[-3] == '0':
                    inputNum = data[data[num+1]]
                    #print(data[data[num+1]]) 
                else:
                    inputNum = data[num+1]
                    #print(data[num+1])
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
    outputs.append(inputNum)
print(max(outputs))
'''
# Part 2
phases = permutations(range(5,10))
outputs = []
for phase in phases:
    data = {p:[int(i) for i in splitFile] for p in phase}
    inputNum = 0
    feedback = False
    halts = 0
    nums = defaultdict(list)
    while halts < 5:
        for inputPhase in phase:
            #data = [int(i) for i in splitFile] 
            input2 = False
            if len(nums[inputPhase]) > 0:
                num = nums[inputPhase][-1]
            else:
                num = 0
            while num < len(data[inputPhase]):
                inst = str(data[inputPhase][num])
                if len(inst) < 4:
                    inst = '0'*(4-len(inst)) + inst
                if inst[-2:] == '03':
                    if not input2 and not feedback:
                        data[inputPhase][data[inputPhase][num+1]] = inputPhase
                        input2 = True
                    else:
                        data[inputPhase][data[inputPhase][num+1]] = inputNum
                    num += 2
                    continue
                elif inst[-2:] == '04':
                    if inst[-3] == '0':
                        inputNum = data[inputPhase][data[inputPhase][num+1]]
                        #print(data[data[num+1]]) 
                    else:
                        inputNum = data[inputPhase][num+1]
                        #print(data[num+1])
                    num += 2
                    nums[inputPhase].append(num)
                    break
                elif inst[-2:] == '99':
                    halts += 1
                    break
                par1 = data[inputPhase][data[inputPhase][num+1]] if inst[-3] == '0' else data[inputPhase][num+1]
                par2 = data[inputPhase][data[inputPhase][num+2]] if inst[-4] == '0' else data[inputPhase][num+2]
                if inst[-2:] == '01':
                    data[inputPhase][data[inputPhase][num+3]] = par1 + par2
                elif inst[-2:] == '02':
                    data[inputPhase][data[inputPhase][num+3]] = par1 * par2
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
                        data[inputPhase][data[inputPhase][num+3]] = 1
                    else:
                        data[inputPhase][data[inputPhase][num+3]] = 0
                elif inst[-2:] == '08':
                    if par1 == par2:
                        data[inputPhase][data[inputPhase][num+3]] = 1
                    else:
                        data[inputPhase][data[inputPhase][num+3]] = 0
                num += 4
        feedback = True
        outputs.append(inputNum)
print(max(outputs))
