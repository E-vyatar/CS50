#include <cs50.h>
#include <stdio.h>
#include<string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;


// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool lock_check(int winner, int loser);


int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
// ranks = voter number, rank = candidate place
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0) // is the candidate name valid?
        {
            ranks[rank] = i; // the candidate name is valid, put their "name" (number) in place
            return true;
        }
    }
    return false; // the candidate name is'nt valid
}

// Update preferences given one voter's ranks
// ranks = voter's choices
void record_preferences(int ranks[])
{
    for (int a = 0; a < candidate_count; a++) // preferred candidate
    {
        for (int b = a + 1; b < candidate_count; b++)
        {
            preferences[ranks[a]][ranks[b]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int a = 0; a < candidate_count; a++)
    {
        for (int b = a + 1; b < candidate_count; b++)
        {
            if (preferences[a][b] != preferences[b][a])
            {
                pair p; // temporary pair holer
                if (preferences[a][b] > preferences[b][a]) // if candidate a won
                {
                    p.winner = a;
                    p.loser = b;
                }
                else // if candidate b won
                {
                    p.winner = b;
                    p.loser = a;
                }
                pairs[pair_count++] = p; // insert data to array
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    pair temp; // temporary place
    for (int i = 0; i < pair_count; i++)
    {
        int place = i; // current place holder
        int cstrenght = preferences[pairs[i].winner][pairs[i].loser] - preferences[pairs[i].loser][pairs[i].winner]; // current place holder
        for (int j = i + 1; j < pair_count; j++)
        {
            int tstrenght = preferences[pairs[j].winner][pairs[j].loser] - preferences[pairs[j].loser][pairs[j].winner]; // checked place wanter
            if (tstrenght > cstrenght) // if wanter has stronger victory
            {
                place = j; // new place holder
                cstrenght = preferences[pairs[j].winner][pairs[j].loser] - preferences[pairs[j].loser][pairs[j].winner]; // new place holder
            }
        }
        // switching places
        temp = pairs[place]; // claer winner old place
        pairs[place] = pairs[i]; // put loser unto winner old place
        pairs[i] = temp; // put winner into loser old place
    }
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        if (!lock_check(pairs[i].winner, pairs[i].loser)) // if there is no cycle
        {
            locked[pairs[i].winner][pairs[i].loser] = true; // lock the pair
        }
    }
    return;
}

bool lock_check(int winner, int loser)
{
    while (winner != -1 && winner != loser)
    {
        bool found = false;
        for (int i = 0; i < candidate_count; i++)
        {
            if (locked[i][winner])
            {
                found = true;
                winner = i;
            }
        }
        if (!found)
        {
            winner = -1;
        }
    }
    if (winner == loser)
    {
        return true;
    }
    return false;
}

// Print the winner of the election
void print_winner(void)
{
    int loser;
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[i][j] == true)
            {
                loser = j;
            }
        }
        if (loser != i)
        {
            printf("winner: %s\n", candidates[i]);
        }
    }
}