#include <stdio.h>
#include <cs50.h>
#include<ctype.h>
#include<string.h>
#include<math.h>

// determine readability level of text
int main(void)
{
    // user input
    string text = get_string("text: ");

    // variables
    float letters = 0;
    int words = 1; // counting spaces
    float sentences = 0;

    // counters
    for (int i = 0, n = strlen(text); i < n; i++)
        if (isalpha(text[i]))
        {
            letters++;
        }
    for (int i = 0, n = strlen(text); i < n; i++)
        if ((text[i]) == ' ')
        {
            words++;
        }
    for (int i = 0, n = strlen(text); i < n; i++)
        if ((text[i]) == '.' || (text[i]) == '!' || (text[i]) == '?')
        {
            sentences++;
        }

    // calculate according to Coleman-Liau index
    float calculation = 0.0588 * letters / words * 100 - 0.296 * sentences / words * 100 - 15.8;
    int result = round(calculation);

    // check and print result
    if (result >= 1 && result < 16)
    {
        printf("Grade %i\n", result);
    }
    else
    {
        if (result < 1)
        {
            printf("Before Grade 1\n");
        }
        else
        {
            printf("Grade 16+\n");
        }
    }
}