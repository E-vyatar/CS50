# Simulate a sports tournament

import csv
import sys
import random

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # open file of ratings to read
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        
        for line in reader:
            # convert rating to int
            line['rating'] = int(line['rating'])
          
            # add information to teams list
            teams.append(line)

    counts = {}
    
    # running the simulation N times
    for i in range(N):
        
        # get a winner of a tournament
        n = simulate_tournament(teams)
        
        # tournament winner already won before
        if n in counts:
            counts[n] += 1
            
        # tournament winner haven't won before
        else:
            counts[n] = 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    
    # simulate round at leat once
    w = simulate_round(teams)
    
    # keep simulating rounds until there is only one winner left at the end of it
    while len(w) != 1:
        w = simulate_round(w)
    return w[0]['team']


if __name__ == "__main__":
    main()