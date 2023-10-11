#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int all_letters(string x); //application for checking key contains only letters
int letter_once(string y); //application for checking key contains each character only once

//substitution
int main(int argc, string argv[])
{
    if (argc == 2) //checking for only one command-line argument
    {
        if (strlen(argv[1]) == 26) //checking key contains exactly 26 characters
        {
            if (all_letters(argv[1]) == 0) //checking key contains only letters
            {
                if (letter_once(argv[1]) == 0) //checking key contains each letter only once
                {
                    string plaintext = get_string("plaintext: "); //user's input
                    string ciphertext = plaintext;
                    for (int i = 0, n = strlen(plaintext); i < n; i++)
                    {
                        int toascii(char plaintext[i]);
                        if (islower(plaintext[i])) //lowercase loop
                        {
                            ciphertext[i] = argv[1][plaintext[i] - 97];
                            ciphertext[i] = tolower(ciphertext[i]);
                        }
                        else if (isupper(plaintext[i])) //uppercase loop
                        {
                            ciphertext[i] = argv[1][plaintext[i] - 65];
                            ciphertext[i] = toupper(ciphertext[i]);
                        }
                    }
                    printf("ciphertext: %s\n", ciphertext); //output
                    return 0;
                }
                else
                {
                    printf("One or more key characters appear more than once. Each character must appear only once\n"); //error: letter uppear more than once in key
                    return 1;
                }
            }
            else
            {
                printf("One or more key characters are invalid. Key must contain only letters\n"); //error: key contains non-letters characters
                return 1;
            }
        }
        else
        {
            printf("Key lenght is invalid. Key must contain exactly 26 letters\n"); //error: invalid key lenght
            return 1;
        }
    }
    else
    {
        printf("Too many arguments\n"); //error: invalid command-line arguments number
        return 1;
    }
}


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

int letter_once(string y)
{
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