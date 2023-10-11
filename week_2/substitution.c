#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>


// cipher text using substitution

// declared functions
int all_letters(string x);
int letter_once(string y);

int main(int argc, string argv[])
{
    if (argc == 2) // checking for only one command-line argument
    {
        if (strlen(argv[1]) == 26) // checking key contains exactly 26 characters
        {
            if (all_letters(argv[1]) == 0) // checking key contains only letters
            {
                if (letter_once(argv[1]) == 0) // checking key contains each letter only once
                {
                    string plaintext = get_string("plaintext: "); // user input
                    string ciphertext = plaintext;

                    // iterate text
                    for (int i = 0, n = strlen(plaintext); i < n; i++)
                    {
                        int toascii(char plaintext[i]);
                        if (islower(plaintext[i])) // lowercase loop
                        {
                            ciphertext[i] = argv[1][plaintext[i] - 97];
                            ciphertext[i] = tolower(ciphertext[i]);
                        }
                        else if (isupper(plaintext[i])) // uppercase loop
                        {
                            ciphertext[i] = argv[1][plaintext[i] - 65];
                            ciphertext[i] = toupper(ciphertext[i]);
                        }
                    }
                    printf("ciphertext: %s\n", ciphertext); // output
                    return 0;
                }
                else // error: letter uppear more than once in key
                {
                    printf("One or more key characters appear more than once. Each character must appear only once\n");
                    return 1;
                }
            }
            else // error: key contains non-letters characters
            {
                printf("One or more key characters are invalid. Key must contain only letters\n");
                return 1;
            }
        }
        else // error: invalid key lenght
        {
            printf("Key lenght is invalid. Key must contain exactly 26 letters\n");
            return 1;
        }
    }
    else // error: invalid number of command-line arguments
    {
        printf("Too many arguments\n");
        return 1;
    }
}


// function for checking key contains only letters
int all_letters(string x)
{
    int letters_char = 0;
    for (int i = 0, n = strlen(x); i < n; i++)
    {
        if (isalpha(x[i]))
        {
            letters_char++;
        }
    }
    
    if (letters_char == 26)
    {
        return 0;
    }
    else
    {
        return 1;
    }
}

// function for checking key contains each character only once
int letter_once(string y)
{
    // match case for all characters
    for (int i = 0; i < 26; i++)
    {
        y[i] = toupper(y[i]);
    }

    int letter_number = 0;
    for (int i = 0; i < 26; i++)
    {
        for (int j = 0; j < 26; j++)
        {
            if (y[i] == y[j])
            {
                letter_number++;
            }
        }
    }
    
    if (letter_number == 26)
    {
        return 0;
    }
    else
    {
        return 1;
    }
}