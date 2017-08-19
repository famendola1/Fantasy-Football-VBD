#!/usr/bin/env python3

import pandas as pd
import numpy as np

file = "projections_2017.csv"

draft_size = 272 # 16 teams, 17 players per team

# Value Over Replacement Player (VORP)

# Sets the VBD based on player position
def set_vbd(row):
    if row[1] == 'QB':
        row[4] = row[3] - replacement_qb
    elif row[1] == 'RB':
        row[4] = row[3] - replacement_rb
    elif row[1] == 'WR':
        row[4] = row[3] - replacement_wr
    elif row[1] == 'TE':
        row[4] = row[3] - replacement_te
    elif row[1] == 'DST':
        row[4] = row[3] - replacement_dst
    elif row[1] == 'K':
        row[4] = row[3] - replacement_k

    return row

# Adjusts the VBD based on the given multiplier
def adjust(row, pos, mult):
    if row[1] == pos:
        row[4] *= mult
    return row

if __name__ == "__main__":
    all_projections = pd.read_csv(file)
    all_projections = all_projections.query("team != 'FA'") # remove free agents
    all_projections = all_projections.sort_values(by='overallRank')
    projections = all_projections.head(draft_size)
    projections.to_csv('test.csv')

    all_positions = ['QB', 'RB', 'WR', 'TE', 'DST', 'K']

    replacement_qb = 0
    replacement_rb = 0
    replacement_wr = 0
    replacement_te = 0
    replacement_dst = 0
    replacement_k = 0

    for pos in all_positions:
        # Query the position players to find the last ranked at that position
        # that would be drafted
        expression = "playerposition == '" + pos +"'"
        draft_pos = projections.query(expression)

        # Get the last rank
        draft_pos = draft_pos.sort_values(by='positionRank')
        last_rank = draft_pos.tail(1)['positionRank'].iloc[0]

        # Special case for defenses in big leagues
        if last_rank != 32 and pos != 'DST':
            expression_2 = "positionRank > " + str(last_rank)

            # Get players by position
            replacement_players = all_projections.query(expression)

            # Get players and sort by rank
            replacement_players = replacement_players.query(expression_2)
            replacement_players = replacement_players.sort_values(by='positionRank')

            # Get the projected points of the first replacement player
            replacement_points = replacement_players.head(1)['points'].iloc[0]
        else:
            replacement_points = draft_pos.tail(1)['points'].iloc[0]

        if pos == 'QB':
            replacement_qb = replacement_points
        elif pos == 'RB':
            replacement_rb = replacement_points
        elif pos == 'WR':
            replacement_wr = replacement_points
        elif pos == 'TE':
            replacement_te = replacement_points
        elif pos == 'DST':
            replacement_dst = replacement_points
        elif pos == 'K':
            replacement_k = replacement_points

    # Extract only the relevant columns
    projections = projections[["player", "playerposition", "adp", "points"]]

    projections["vbd"] = 0
    projections = projections.apply(func=set_vbd, axis=1, broadcast=True)
    projections = projections.sort_values(by="vbd", ascending=False)
    projections.to_csv("original.csv")

    while True:
        print("What would you like to do?")
        print("-- Type 'remove [Player Name]' to remove a player")
        print("-- Type 'adjust [position] [multiplier]' to adjust VBD")
        print("-- Type 'draft [position]' to display the player to draft")
        print("-- Type 'display [position]' to show the top 10 players available")
        print("-- Type 'exit' to leave")

        choice = input()
        choice = choice.split(" ")
        print()

        if choice[0] == 'remove' or choice[0] == 'r':
            if len(choice) == 3:
                name = choice[1] + " " + choice[2]
                name = name.strip()
                expression = "player != '" + name + "'"
                projections.query(expr=expression, inplace=True)
                print(name + " was removed")
                print()
            else:
                print("Invalid use of remove")
                print()
        elif choice[0] == 'adjust' or choice[0] == 'a':
            if len(choice) == 3:
                pos = choice[1].upper()
                mult = float(choice[2])

                projections = projections.apply(func=adjust, axis=1, args=(pos, mult), broadcast=True)
                projections.sort_values(by="vbd", inplace=True, ascending=False)
                projections.to_csv("updated.csv")
                print("VBD for " + pos + " was adjusted")
                print()
            else:
                print("Invlid use of adjust")
                print()
        elif choice[0] == 'draft' or choice[0] == 'dr':
            if len(choice) == 2:
                pos = choice[1].upper()
                print()
                if pos == 'ANY':
                    print(projections.head(1))
                else:
                    expression = "playerposition == '" + pos + "'"
                    players = projections.query(expression)
                    print(players.head(1))
                print()
            else:
                print("Invalid use of draft")
                print()
        elif choice[0] == 'display' or choice[0] == 'di':
            if len(choice) == 2:
                pos = choice[1].upper()
                print()
                if pos == 'ALL':
                    print(projections.head(10))
                else:
                    expression = "playerposition == '" + pos + "'"
                    players = projections.query(expression)
                    print(players.head(10))
                print()
            else:
                print("Invalid use of display")
                print()
        elif choice[0] == 'exit' or choice[0] == 'e':
            print("Good Luck This Season :)")
            break
