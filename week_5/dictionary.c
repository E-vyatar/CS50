// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <wchar.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 500;

// Hash table
node *table[N];

//number of words in dictionary
int word_count = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{

    unsigned int h = hash(word);
    int x = floor(4294967295 / N);
    int y = 0;
    for (int i = 0; i < N - 1; i++)
    {
        if (x * i <= h && h < x * (i + 1))
        {
            y = i;
        }
    }
    if (h >= x * (N - 1))
    {
        y = N - 1;
    }
    node *cursor = table[y]; //cursor points to the same node as the header of the word's section
    if (cursor ==
        NULL) //cursor doesn't point to anything, meaning there aren't any words at all in that section, especially the one we're checking
    {
        return false;
    }
    while (cursor != NULL) //as long as cursor points to some node
    {
        if (strcasecmp(word, cursor->word) ==
            0) //the word in check and the word in the node cursor is pointing at are the same, ignoring case
        {
            return true;
        }
        else
        {
            cursor = cursor->next; //make cursor point to what the current node cursor points to points to, i.e. the next word in this section
        }
    }
    return false; //the word in check wasn't in the section it's supposed to be, therefore it's not in the dictionary
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Djb2 hash function
    {
        unsigned int hash = 5381;
        int c;
        while ((c = *word++))
        {
            hash = ((hash << 5) + hash) + tolower(c);    /* hash * 33 + c */
        }
        return hash;
    }
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //open dictionary file
    FILE *D = fopen(dictionary, "r");
    char word[LENGTH + 1]; //placeholder for a word in check
    while (fscanf(D, "%s", word) != EOF) //as long as the file hadn't reach its end, keep checking each string
    {
        node *w = malloc(sizeof(node)); //ponter to node
        strcpy(w->word, word); //insert word in load to the node that is pointed
        unsigned int h = hash(word);
        int x = floor(4294967295 / N);
        int y = 0;
        for (int i = 0; i < N - 1; i++)
        {
            if (x * i <= h && h < x * (i + 1))
            {
                y = i;
            }
        }
        if (h >= x * (N - 1))
        {
            y = N - 1;
        }
        node *n = table[y]; //n is a cursor
        if (n == NULL) //no word had been inserted in this section yet
        {
            table[y] = w; //make the header of this section point to the node that holds the word in load
            w->next = NULL; //set the node pointer part to not pointing to anything
            word_count++;
        }
        else //there are already word/s in this section
        {
            while (n->next != NULL) //as long as cursor hadn't reached the end of the section
            {
                n = n->next; //move cursor to the next word
            }
            n->next = w; //make the pointer part of the last word in this section point to the node that holds the word in load
            w->next = NULL; //set the node pointer part to not pointing to anything
            word_count++;
        }
    }
    if (fclose(D) == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N + 1; i++)
    {
        node *cursor = table[i];
        node *tmp = cursor;
        while (cursor != NULL)
        {
            tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}