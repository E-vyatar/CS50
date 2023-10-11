#include <stdio.h>
#include <cs50.h>

// print mario pyramid, i.e. for height 4 print
//    # #
//   ## ##
//  ### ###
// #### ####


int main(void)
{
    // user input
    int n;
    do
    {
        n = get_int("height: ");
    }
    while (n < 1 || n > 8); // only accept range 1-8 (inclusive)

    // print lines
    for (int i = 0; i < n; i++)
    {
        // print spaces before first #
        for (int h = 0; h < n - i - 1; h++)
        {
            printf(" ");
        }

        // print left side of line
        for (int j = 0; j < i + 1; j++)
        {
            printf("#");
        }

        // print gap
        printf("  ");

        // print right side of line
        for (int g = 0; g < i + 1; g++)
        {
            printf("#");
        }
        
        printf("\n");
    }
}