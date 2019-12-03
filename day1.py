from pathlib import Path

inputFile = Path("inputs/input-01-01.txt")

# PART 1
fuel = 0
with inputFile.open() as f:
    for line in f:
        fuel += int(line) // 3 - 2

print(fuel)

# PART 2
def get_fuel(fuel):
    if fuel <= 0:
        return 0
    return fuel + get_fuel(fuel // 3 - 2)

fuel = 0
with inputFile.open() as f:
    for line in f:
        fuel += get_fuel(int(line) // 3 - 2)

print(fuel)
