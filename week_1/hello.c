#include <stdio.h>
#include <cs50.h>

// say hello
int main(void)
{
    string name = get_string("What is your name?\n");
    printf("Hello, %s, nice to meet you!\n", name);
}