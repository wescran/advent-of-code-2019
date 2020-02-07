import copy
def get_command(cmd,cmds):
    if cmd.startswith('take'):
        return cmds['take'](cmd[5:]).copy() #assuming 'take ITEM'
    elif cmd.startswith('drop'):
        return cmds['drop'](cmd[5:]).copy()
    return cmds[cmd].copy()

def intcode(prog, commands):
    data = prog.copy()
    outputs = []
    num = 0
    base = 0
    running = False
    while True:
        # make sure all instrctions are of length 4
        inst = str(data[num])
        if len(inst) < 5:
            inst = '0'*(5-len(inst)) + inst
        
        # these are for opcodes that have 2 or less params    
        if inst[-2:] == '03':
            if not running or not cmd:
                while True:
                    try:
                        command = input("Please give a command: ")
                        cmd = get_command(command, commands)
                        break
                    except:
                        print("Error with input, try again")
                inputNum = cmd.pop(0)
                running = True
            else:
                inputNum = cmd.pop(0)
            if inst[-3] == '0':
                data[data[num+1]] = inputNum 
            else:
                data[data[num+1] + base] = inputNum
            num += 2
            continue
        elif inst[-2:] == '04':
            if inst[-3] == '0':
                val = data[data[num+1]]
            elif inst[-3] == '1':
                val = data[num+1]
            else:
                val = data[data[num+1] + base]
            num += 2
            if val == 10:
                outputs.append(chr(val))
                yield outputs
                outputs = []
            else:
                outputs.append(chr(val))
            continue
        elif inst[-2:] == '09':
            if inst[-3] == '0':
                val = data[data[num+1]]
            elif inst[-3] == '1':
                val = data[num+1]
            else:
                val = data[data[num+1] + base]
            base = base + val  
            num += 2
            continue
        elif inst[-2:] == '99':
            running = False
            print('Done')
            break
        
        # this part for instructions with more than 2 params
        # param 1
        if inst[-3] == '0':
            try:
                par1 = data[data[num+1]]
            except IndexError:
                data.extend([0 for _ in range(len(data), data[num+1] +1)])
                par1 = data[data[num+1]]
        elif inst[-3] == '1':
            try:
                par1 = data[num+1]
            except IndexError:
                data.extend([0 for _ in range(len(data), num+1 +1)])
                par1 = data[num+1]
        else:
            try:
                par1 = data[data[num+1] + base]
            except IndexError:
                data.extend([0 for _ in range(len(data), data[num+1] +base +1)])
                par1 = data[data[num+1] + base]

        # param 2
        if inst[-4] == '0':
            try:
                par2 = data[data[num+2]]
            except IndexError:
                data.extend([0 for _ in range(len(data), data[num+2] +1)])
                par2 = data[data[num+2]]
        elif inst[-4] == '1':
            try:
                par2 = data[num+2]
            except IndexError:
                data.extend([0 for _ in range(len(data), num+2 +1)])
                par2 = data[num+2]
        else:
            try:
                par2 = data[data[num+2] + base]
            except IndexError:
                data.extend([0 for _ in range(len(data), data[num+2]+base +1)])
                par2 = data[data[num+2] + base]

        if inst[-2:] == '01':
            val = par1 + par2
            if inst[-5] == '0':
                try:
                    data[data[num+3]] = val
                except IndexError:
                    data.extend([0 for _ in range(len(data), data[num+3] +1)])
                    data[data[num+3]] = val
            else:
                try:
                    data[data[num+3] + base] = val
                except IndexError:
                    data.extend([0 for _ in range(len(data), data[num+3]+base +1)])
                    data[data[num+3] + base] = val
        elif inst[-2:] == '02':
            val = par1 * par2
            if inst[-5] == '0':
                try:
                    data[data[num+3]] = val
                except IndexError:
                    data.extend([0 for _ in range(len(data), data[num+3] +1)])
                    data[data[num+3]] = val
            else:
                try:
                    data[data[num+3] + base] = val
                except IndexError:
                    data.extend([0 for _ in range(len(data), data[num+3]+base +1)])
                    data[data[num+3] + base] = val
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
                if inst[-5] == '0':
                    try:
                        data[data[num+3]] = 1
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3] +1)])
                        data[data[num+3]] = 1
                else:
                    try:
                        data[data[num+3] + base] = 1
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3]+base +1)])
                        data[data[num+3]+base] = 1
            else:
                if inst[-5] == '0':
                    try:
                        data[data[num+3]] = 0
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3] +1)])
                else:
                    try:
                        data[data[num+3] + base] = 0
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3]+base +1)])
        elif inst[-2:] == '08':
            if par1 == par2:
                if inst[-5] == '0':
                    try:
                        data[data[num+3]] = 1
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3] +1)])
                        data[data[num+3]] = 1
                else:
                    try:
                        data[data[num+3] + base] = 1
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3]+base +1)])
                        data[data[num+3]+base] = 1
            else:
                if inst[-5] == '0':
                    try:
                        data[data[num+3]] = 0
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3] +1)])
                else:
                    try:
                        data[data[num+3] + base] = 0
                    except IndexError:
                        data.extend([0 for _ in range(len(data), data[num+3]+base +1)])
        num += 4
