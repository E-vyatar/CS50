#include <stdio.h>
#include <cs50.h>

//mario

int main(void)
{
    //question
    int n;
    do
    {
        n = get_int("height: ");
    }
    while (n < 1 || n > 8);
    //number of lines
    for (int i = 0; i < n; i++)
    {
        //number of spaces before #
        for (int h = 0; h < n - i - 1; h++)
        {
            printf(" ");
        }
        //number of #
        for (int j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        printf("  ");
        //number of #2
        for (int g = 0; g < i + 1; g++)
        {
            printf("#");
        }
        printf("\n");
    }
}