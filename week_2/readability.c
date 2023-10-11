#include <stdio.h>
#include <cs50.h>
#include<ctype.h>
#include<string.h>
#include<math.h>

//readability
int main(void)
{
    //user's input
    string text = get_string("text: ");
    //variables
    float letters = 0;
    int words = 1;
    float sentences = 0;
    //counters
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
    //formula
    float calculation = 0.0588 * letters / words * 100 - 0.296 * sentences / words * 100 - 15.8;
    int result = round(calculation);
    //result
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