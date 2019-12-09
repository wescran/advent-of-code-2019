from pathlib import Path
from collections import defaultdict
inputFile = Path("inputs/input-06-01.txt")
data = inputFile.read_text().rstrip().split("\n")

'''
# Part 1
def count_orbits(dir_list, obj):
    if not dir_list[obj]:
        return 0
    return 1 + count_orbits(dir_list, dir_list[obj][0])

dir_count = 0
dir_list = defaultdict(list)
for orbit in data:
    dir_count += 1
    dir_list[orbit[4:]].append(orbit[:3])
ind_count = 0
for orbit in data:
    if dir_list[orbit[:3]]:
        ind_count += count_orbits(dir_list, orbit[:3])    

print(dir_count + ind_count)
'''
# Part 2
def get_orbits(dir_list, obj):
    if not dir_list[obj]:
        return ["COM"]
    l = get_orbits(dir_list, dir_list[obj][0])
    l.append(obj)
    return l

dir_count = 0
dir_list = defaultdict(list)
for orbit in data:
    dir_count += 1
    dir_list[orbit[4:]].append(orbit[:3])

Y = get_orbits(dir_list, 'YOU')
S = get_orbits(dir_list, 'SAN')
step_count = -1
check = defaultdict(list)
for i,j in zip(reversed(Y), reversed(S)):
    print(i,j,step_count)
    check[i].append(step_count)
    check[j].append(step_count)
    if len(check[i]) > 1:
        print(sum(check[i]),i)
        break
    elif len(check[j]) > 1:
        print(sum(check[j]),j,check[j])
        break
    step_count += 1
