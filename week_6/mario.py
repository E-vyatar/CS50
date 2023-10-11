from cs50 import get_int

# question
while True:
    height = get_int("Height: ")
    if height in [1, 2, 3, 4, 5, 6, 7, 8]:
        break
  
# number of lines
for i in range(height):
    
    # number of spaces before #    
    for j in range(height - i - 1):
        print(" ", end="")
    
    # number of #        
    for h in range(i + 1):
        print("#", end="")
    
    # space        
    print("  ", end="")
    
    # number of #2    
    for g in range(i + 1):
        print("#", end="")
    
    # new line
    print("")