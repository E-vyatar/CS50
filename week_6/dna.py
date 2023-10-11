import csv
import sys

# global variables
global_counter = 0
highest_counter = 0
text_cursor = 0


def main():
    # valid command-line argument
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # database list
    database = []

    # result list
    result = []

    # open csv file and make keys list
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)

        dict_from_csv = dict(list(reader)[0])
        keys_list = list(dict_from_csv.keys())

    # open csv file and convert STRs into integers
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            for i in range(1, len(keys_list)):
                line[keys_list[i]] = int(line[keys_list[i]])

            # write csv file information into database
            database.append(line)

    # open txt file and read
    sequence = open(sys.argv[2], "r").read()

    # using global key word
    global global_counter
    global highest_counter
    global text_cursor

    # loop over all STRs
    for i in range(1, len(keys_list)):

        # current STR
        x = keys_list[i]

        # initialize global variables
        global_counter = 0
        highest_counter = 0
        text_cursor = 0

        # search through text
        while text_cursor < len(sequence):

            # search for first letter of STR
            if sequence[text_cursor] == x[0]:

                # check for STR
                if STR_Checker(sequence[text_cursor:text_cursor + len(x) + 1], x) == True:

                    # count consecutive
                    consecutive_counter(sequence[text_cursor:len(sequence) + 1], x)
                    text_cursor = text_cursor + (len(x) * global_counter)
                    global_counter = 0

                else:
                    text_cursor += 1

            else:
                text_cursor += 1

        result.append(highest_counter)

    # compare
    # loop over people
    for i in range(len(database)):

        # loop over STRs
        for j in range(1, len(keys_list)):

            # search for no match
            if database[i][keys_list[j]] != result[j - 1]:
                break

            # no no match found so this is the person
            if j == len(keys_list) - 1:
                sys.exit(database[i]['name'])

    # no one matched
    sys.exit("No match")


# function for searching specific STR in text
def STR_Checker(txt, STR):
    
    # breakpoint1 - end of STR, meaning there is a match
    if len(STR) == 0:
        return True
    
    # breakpoint2 - end of txt
    if len(txt) == 0:
        return False

    # compare first letters of text and STR
    if txt[0] == STR[0]:

        # recursion
        if STR_Checker(txt[1:len(txt) + 1], STR[1:len(STR) + 1]) == True:
            return True

        # no match
        else:
            return False


# function for counting consecutive repeats of specific STR
def consecutive_counter(txt, STR):
    
    # breakpoint - end of text or not enough letters remain
    # in text for another STR
    if len(txt) == 0 or len(txt) == len(STR) - 1:
        return

    # searching for STR
    if STR_Checker(txt, STR) == True:

        # recursion
        consecutive_counter(txt[len(STR):len(txt) + 1], STR)

        # update global variables
        global global_counter
        global highest_counter
        global_counter += 1
        if global_counter > highest_counter:
            highest_counter = global_counter
            return

    else:
        return


main()