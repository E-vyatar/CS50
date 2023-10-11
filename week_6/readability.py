from cs50 import get_string

# user's input
text = get_string("Text: ")

# variables
letters = 0
words = 1
sentences = 0

# letters counter
for i in text:
    if (i.isalpha()) == True:
        letters += 1

# words counter
for i in text:
    if (i == " "):
        words += 1

# sentences counter
for i in text:
    if (i == "." or i == "!" or i == "?"):
        sentences += 1

# formula
calculation = round(0.0588 * letters / words * 100 - 0.296 * sentences / words * 100 - 15.8)

# result
if calculation >= 1 and calculation < 16:
    print(f"Grade {calculation}")
elif calculation < 1:
    print("Before Grade 1")
else:
    print("Grade 16+")