from cs50 import get_float

# user's input
while True:
    a = get_float("Change owed: ")
    if a >= 0:
        break
    
# input adjastment
A = round(a * 100)

# coins counter
i = 0

# 25 cents
while A - 25 >= 0:
    A -= 25
    i += 1
    
# 10 cents
while A - 10 >= 0:
    A -= 10
    i += 1

# 5 cents
while A - 5 >= 0:
    A -= 5
    i += 1

# 1 cents
while A - 1 >= 0:
    A -= 1
    i += 1

# output
print(f"{i}")