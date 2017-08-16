import pandas as pd
import numpy as np

file = "ffa_customrankings2017-0.csv"

draft_size = 272 # 16 teams, 17 players per team

# Value Over Replacement Player (VORP)

# Sets the VBD based on player position
def set_vbd(row):
    if row[1] == 'QB':
        row[3] = row[2] - replacement_qb
    elif row[1] == 'RB':
        row[3] = row[2] - replacement_rb
    elif row[1] == 'WR':
        row[3] = row[2] - replacement_wr
    elif row[1] == 'TE':
        row[3] = row[2] - replacement_te
    elif row[1] == 'DST':
        row[3] = row[2] - replacement_dst
    elif row[1] == 'K':
        row[3] = row[2] - replacement_k

    return row

# Adjusts the VBD based on the given multiplier
def adjust(row, pos, mult):
    if row[1] == pos:
        row[3] *= mult
    return row

if __name__ == "__main__":
    all_projections = pd.read_csv(file)
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
        expression = "playerposition == '" + pos +"'"
        draft_pos = projections.query(expression)

        # Get the last rank
        draft_pos = draft_pos.sort_values(by='positionRank')
        last_rank = draft_pos.tail(1)['positionRank'].iloc[0]

        # Get the projected points of the first replacement player
        expression = "positionRank > " + str(last_rank)
        replacement_players = all_projections.query(expression)
        replacement_players = replacement_players.sort_values(by='positionRank')
        replacement_points = replacement_players.head(1)['points'].iloc[0]

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
    projections = projections[["player", "playerposition", "points"]]

    projections["vbd"] = 0
    projections = projections.apply(func=set_vbd, axis=1, broadcast=True)
    projections = projections.sort_values(by="vbd", ascending=False)
    projections.to_csv("original.csv")

    while True:
        print("What would you like to do?")
        print("-- Type 'remove' to remove a player")
        print("-- Type 'adjust' to adjust VBD")
        print("-- Type 'draft' to display the player to draft")
        print("-- Type 'display' to show the top 10 players available")
        print("-- Type 'exit' to leave")

        choice = input()
        print()

        if choice == 'remove':
            name = input("Name?: ")
            expression = "player != '" + name + "'"
            projections.query(expr=expression, inplace=True)
            print(name + " was removed")
            print()
        elif choice == 'adjust':
            pos = input("Position? (QB, RB, WR, TE, DST, K): ")
            mult = float(input("Multiplier?: "))

            projections = projections.apply(func=adjust, axis=1, args=(pos, mult), broadcast=True)
            projections.sort_values(by="vbd", inplace=True, ascending=False)
            projections.to_csv("updated.csv")
            print("VBD was adjusted")
            print()
        elif choice == 'draft':
            pos = input("Position? (ANY, QB, RB, WR, TE, DST, K): ")
            print()
            if pos == 'ANY':
                print(projections.head(1))
            else:
                expression = "playerposition == '" + pos + "'"
                players = projections.query(expression)
                print(players.head(1))
            print()
        elif choice == 'display':
            pos = input("Position? (ALL, QB, RB, WR, TE, DST, K): ")
            print()
            if pos == 'ALL':
                print(projections.head(10))
            else:
                expression = "playerposition == '" + pos + "'"
                players = projections.query(expression)
                print(players.head(10))
            print()
        elif choice == 'exit':
            print("Good Luck This Season :)")
            break
