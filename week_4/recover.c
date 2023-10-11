#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    //incorrect number og command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image/n");
        return 1;
    }
    //correct number og command-line arguments
    
    //Preparations
    FILE *new_file; //files pointer
    FILE *memory_card = fopen(argv[1], "r"); //memory card pointer
    typedef uint8_t BYTE;
    BYTE x[512]; //buffer
    int file_name_count = 0; //"file names" counter

    //while reading the card
    while ((fread(&x, sizeof(BYTE), 512, memory_card)) == 512)
    {
        //start of a jpeg file
        if (x[0] == 0xff && x[1] == 0xd8 && x[2] == 0xff && (x[3] & 0xf0) == 0xe0)
        {
            //first jpeg
            if (file_name_count == 0)
            {
                char filename[8];
                sprintf(filename, "%03i.jpg", file_name_count);
                new_file = fopen(filename, "w");
                file_name_count++;
            }
            //not first jpeg
            else
            {
                fclose(new_file);
                char filename[8];
                sprintf(filename, "%03i.jpg", file_name_count);
                new_file = fopen(filename, "w");
                file_name_count++;
            }
        }
        //writing the image
        if (file_name_count > 0)
        {
            fwrite(&x, sizeof(BYTE), 512, new_file);
        }
    }

}
