#include <stdio.h>
#include <cs50.h>
#include <math.h>

//cash

int main(void)
{
    //user's input
    float N;
    do
    {
        N = get_float("Change owed: ");
    }
    while (N < 0);
    //input adjastment
    int n = round(N * 100);
    //coins counter
    int i = 0;
    //25 cents
    while (n - 25 >= 0)
    {
        n = n - 25;
        i = i + 1;
    }
    // 10 cents
    while (n - 10 >= 0)
    {
        n = n - 10;
        i = i + 1;
    }
    //5 cents
    while (n - 5 >= 0)
    {
        n = n - 5;
        i = i + 1;
    }
    //1 cents
    while (n - 1 >= 0)
    {
        n = n - 1;
        i = i + 1;
    }
    //output
    printf("%i\n", i);
}