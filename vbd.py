import pandas as pd
import numpy as np

file = "ffa_customrankings2017-0.csv"

draft_size = 272 # 16 teams, 17 players per team
projections = pd.read_csv(file)
projections = projections.head(draft_size)

projections = projections[["player", "playerposition", "points"]]

projections["vbd"] = projections["points"] - np.average(projections["points"])
projections
projections.sort_values(by="vbd", inplace=True, ascending=False)
projections.to_csv("original.csv")

def adjust(row, pos, mult):
    if row[1] == pos:
        row[3] *= mult
    return row

on = True
while on:
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
        pos = input("Position?: ")
        expression = "player != '" + name + "'"
        projections.query(expr=expression, inplace=True)
        print(name + " was removed")
        print()
    elif choice == 'adjust':
        pos = input("Position?: ")
        mult = float(input("Multiplier?: "))

        projections = projections.apply(func=adjust, axis=1, args=(pos, mult), broadcast=True)
        projections.sort_values(by="vbd", inplace=True, ascending=False)
        projections.to_csv("updated.csv")
        print("VBD was adjusted")
        print()
    elif choice == 'draft':
        pos = input("Position? (ANY, QB, WR, RB, DST, K, TE): ")
        print()
        if pos == 'ANY':
            print(projections.head(1))
        else:
            expression = "playerposition == '" + pos + "'"
            players = projections.query(expression)
            print(players.head(1))
        print()
    elif choice == 'display':
        pos = input("Position? (ALL, QB, WR, RB, DST, K, TE): ")
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
        on = False
