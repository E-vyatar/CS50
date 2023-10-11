#include <stdio.h>
#include <cs50.h>

// say hello using user name
int main(void)
{
    // get user input
    string name = get_string("What is your name?\n");

    // print using user input
    printf("Hello, %s, nice to meet you!\n", name);
}