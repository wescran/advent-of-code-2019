# range is 246515-739105
# 246666 must be first number, start
# 699999 is last possible in range, end
# Part 1
def checkDigit(number):
    if number // 10 == 0:
        return number,False
    remainder,digit = divmod(number,10)
    prev_digit,pair = checkDigit(remainder)
    if not prev_digit:
        return False, pair
    if digit < prev_digit:
        return False,pair
    if digit == prev_digit and not pair:
        return digit,digit
    return digit,pair

    
count = 0
for num in range(246666, 700000):
    digit,pair= checkDigit(num)
    if digit and pair:
        count+=1
print(count)
'''
# Part 2
def checkDigit(number):
    if number // 10 == 0:
        return number,False,[]
    remainder,digit = divmod(number,10)
    prev_digit,pair,check = checkDigit(remainder)
    if not prev_digit:
        return False, pair,check
    if digit < prev_digit:
        return False,pair,check
    if digit == prev_digit and not pair and digit not in check:
        check.append(digit)
        return digit,digit,check
    if digit == prev_digit and digit == pair and digit in check:
        return digit,False,check
    return digit,pair,check

    
count = 0
for num in range(246666, 700000):
    digit,pair,check = checkDigit(num)
    if digit and pair:
        count+=1
print(count)
'''
