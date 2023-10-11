#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++) //row
    {
        for (int w = 0; w < width; w++) //column
        {
            int average = round((image[h][w].rgbtRed + image[h][w].rgbtGreen + image[h][w].rgbtBlue) / 3.0); //average
            image[h][w].rgbtRed = average; //convert red
            image[h][w].rgbtGreen = average; //convert green
            image[h][w].rgbtBlue = average; //convert blue
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++) //row
    {
        for (int w = 0; w < width; w++) //column
        {
            int sepired = round(.393 * image[h][w].rgbtRed + .769 * image[h][w].rgbtGreen + .189 * image[h][w].rgbtBlue); //calculating red
            if (sepired > 255) //max red
            {
                sepired = 255;
            }
            int sepigreen = round(.349 * image[h][w].rgbtRed + .686 * image[h][w].rgbtGreen + .168 * image[h][w].rgbtBlue); //calculating green
            if (sepigreen > 255) //max green
            {
                sepigreen = 255;
            }
            int sepiblue = round(.272 * image[h][w].rgbtRed + .534 * image[h][w].rgbtGreen + .131 * image[h][w].rgbtBlue); //calculating blue
            if (sepiblue > 255) //max blue
            {
                sepiblue = 255;
            }
            image[h][w].rgbtRed = sepired; //convert red
            image[h][w].rgbtGreen = sepigreen; //convert green
            image[h][w].rgbtBlue = sepiblue; //convert blue
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++) //row
    {
        for (int w = 0; w < floor(width / 2.0); w++) //column to the middle
        {
            RGBTRIPLE temp = image[h][w]; //storing original value
            image[h][w] = image[h][width - 1 - w]; //inserting matching value from the other side to origanl value's place
            image[h][width - 1 - w] = temp; //inserting origanl value to matching value from the other side's place
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //creating temp for original values
    RGBTRIPLE temp[height][width];
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            temp[h][w] = image[h][w];
        }
    }
    for (int h = 0; h < height; h++) //row
    {
        for (int w = 0; w < width; w++) //column
        {
            float block_count = 0;
            int red = 0;
            int green = 0;
            int blue = 0;
            for (int r = h - 1; r < h + 2; r++) //row
            {
                if (r != -1 && r != height) //row edges
                {
                    for (int c = w - 1; c < w + 2; c++) //column
                    {
                        if (c != -1 && c != width) //column edges
                        {
                            block_count++;
                            red = red + temp[r][c].rgbtRed; //calculating red
                            green = green + temp[r][c].rgbtGreen; //calculating green
                            blue = blue + temp[r][c].rgbtBlue; //calculating blue
                        }
                    }
                }
            }
            image[h][w].rgbtRed = round(red / block_count); //convert red
            image[h][w].rgbtGreen = round(green / block_count); //convert green
            image[h][w].rgbtBlue = round(blue / block_count); //convert blue
        }
    }
    return;
}
