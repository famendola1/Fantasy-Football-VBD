#!/usr/bin/env python3

import pandas as pd
import numpy as np
import sys

# Value Over Replacement Player (VORP)

# Sets the VBD based on player position
def set_vbd(row):
    if row["position"] == 'QB':
        row["vbd"] = row["points"] - replacement_qb
    elif row["position"] == 'RB':
        row["vbd"] = row["points"] - replacement_rb
    elif row["position"] == 'WR':
        row["vbd"] = row["points"] - replacement_wr
    elif row["position"] == 'TE':
        row["vbd"] = row["points"] - replacement_te
    elif row["position"] == 'DST':
        row["vbd"] = row["points"] - replacement_dst
    elif row["position"] == 'K':
        row["vbd"] = row["points"] - replacement_k

    return row

# Sets points above average
def set_poa(row):
    if row["position"] == 'QB':
        row["poa"] = row["vbd"] - avg_qb
    elif row["position"] == 'RB':
        row["poa"] = row["vbd"] - avg_rb
    elif row["position"] == 'WR':
        row["poa"] = row["vbd"] - avg_wr
    elif row["position"] == 'TE':
        row["poa"] = row["vbd"] - avg_te
    elif row["position"] == 'DST':
        row["poa"] = row["vbd"] - avg_dst
    elif row["position"] == 'K':
        row["poa"] = row["vbd"] - avg_k

    return row

# Adjusts the VBD based on the given multiplier
def adjust(row, pos, mult):
    if row["position"] == pos:
        row["vbd"] *= mult
    return row

if __name__ == "__main__":
    draft_size = int(sys.argv[1]) * int(sys.argv[2])
    file = sys.argv[3]

    # Read csv file and prepare data for use
    all_projections = pd.read_csv(file)

    # remove free agents and defense
    all_projections = all_projections.query(
        "team != 'FA' and position != 'DB' and position != 'DL' and position != 'LB'")

    all_projections = all_projections.sort_values(by='overallRank')
    projections = all_projections.head(draft_size)

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
        expression = "position == '" + pos + "'"
        draft_pos = projections.query(expression)

        # Get the last rank in the draft
        draft_pos = draft_pos.sort_values(by='positionRank')
        last_rank = draft_pos.tail(1)['positionRank'].iloc[0]

        # Special case for defenses
        if last_rank != 32 and pos != 'DST':
            expression_2 = "positionRank > " + str(last_rank)

            # Get players by position
            replacement_players = all_projections.query(expression)

            # Get players and sort by rank
            replacement_players = replacement_players.query(expression_2)
            replacement_players = replacement_players.sort_values(
                by='positionRank')

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
    projections = projections[["player", "position", "team", "adp", "points"]]

    projections["vbd"] = 0
    projections = projections.apply(
        func=set_vbd, axis=1, result_type='broadcast')
    projections = projections.sort_values(by="vbd", ascending=False)

    # Calculate the points above average for vbd
    avg_qb = np.mean(projections.query("position == 'QB'")['vbd'])
    avg_rb = np.mean(projections.query("position == 'RB'")['vbd'])
    avg_wr = np.mean(projections.query("position == 'WR'")['vbd'])
    avg_te = np.mean(projections.query("position == 'TE'")['vbd'])
    avg_dst = np.mean(projections.query("position == 'DST'")['vbd'])
    avg_k = np.mean(projections.query("position == 'K'")['vbd'])

    projections["poa"] = 0
    projections = projections.apply(
        func=set_poa, axis=1, result_type='broadcast')

    projections.to_csv("original.csv", index=False)

    while True:
        print("> ", end=" ")
        choice = input()
        choice = choice.split(" ")
        print()

        if choice[0] == 'remove' or choice[0] == 'r':
            if len(choice) == 3:
                name = choice[1] + " " + choice[2]
                name = name.strip()
                expression = "player != '" + name + "'"
                projections.query(expr=expression, inplace=True)
                projections.to_csv("updated.csv", index=False)
                print(name + " was removed")
                print()
            else:
                print("Invalid use of remove")
                print()
        elif choice[0] == 'adjust' or choice[0] == 'a':
            if len(choice) == 3:
                pos = choice[1].upper()
                mult = float(choice[2])

                projections = projections.apply(
                    func=adjust, axis=1, args=(pos, mult), result_type='broadcast')
                projections.sort_values(
                    by="vbd", inplace=True, ascending=False)
                projections.to_csv("updated.csv")
                print("VBD for " + pos + " was adjusted")
                print()
            else:
                print("Invalid use of adjust")
                print()
        elif choice[0] == 'draft' or choice[0] == 'dr':
            if len(choice) == 2:
                pos = choice[1].upper()
                print()
                if pos == 'ANY':
                    print(projections.head(1))
                else:
                    expression = "position == '" + pos + "'"
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
                    proj_poa = projections.sort_values(
                        by="poa", ascending=False)
                    print(proj_poa.head(10))
                else:
                    expression = "position == '" + pos + "'"
                    players = projections.query(expression)
                    print(players.head(10))
                print()
            else:
                print("Invalid use of display")
                print()
        elif choice[0] == 'search' or choice[0] == 's':
            if len(choice) == 3:
                name = choice[1] + " " + choice[2]
                name = name.strip()
                expression = "player == '" + name + "'"
                player = projections.query(expression)
                print(player)
                print()
            else:
                print("Invalid use of search")
                print()
        elif choice[0] == 'load' or choice[0] == 'l':
            try:
                projections = pd.read_csv(choice[1])
            except FileNotFoundError:
                print("File not found")
                print()
        elif choice[0] == 'help' or choice[0] == 'h':
            print("What would you like to do?")
            print("-- Type 'remove [Player Name]' to remove a player")
            print("-- Type 'adjust [position] [multiplier]' to adjust VBD")
            print("-- Type 'draft [position]' to display the player to draft")
            print(
                "-- Type 'display [position]' to show the top 10 players available")
            print("-- Type 'search [Player Name]' to search for a player")
            print("-- Type 'load [file]' to load the data from this file")
            print("-- Type 'help' to view this page")
            print("-- Type 'exit' to leave")
            print()
        elif choice[0] == 'exit' or choice[0] == 'e':
            print("Good Luck This Season :)")
            break
        else:
            print("Ivalid command. Type 'help' to view options.")
            print()
