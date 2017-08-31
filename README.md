# Fantasy Football Value Based Drafting
Last Updated: 8/30/2017

## [What is Value Based Drafting (VBD)?](https://www.fantasypros.com/2017/06/what-is-value-based-drafting/)
If the goal were just to find the highest scoring players every year, you would draft a team full of quarterbacks—they were 23 of the top 30 in fantasy points last year. Obviously, no league is set up this way.

In most leagues, you can only start one quarterback, so the key question becomes how much better your quarterback is than your opponent’s. And how much better your two running backs are than your opponent’s running backs. And so on.

Enter VBD. In short, the idea is that a player’s value isn’t based on how many total points he scores. Rather, it is based on how much more he scores than the “baseline” player at his position. VBD encapsulates a number of different ways to set that baseline, but for our purposes, there are three types of VBD:

* Value Over Replacement Player (VORP): How much better is [insert RB] than the best running back available on waivers?
* Value Over Last Starter (VOLS): How much better is [insert RB] than the last starting running back?  
* Value Over Next Available (VONA): How much better is [insert RB] than the best running back available at your next pick?

VBD isn’t perfect. It relies on generating accurate player projections and choosing the correct baseline, both Herculean tasks (if Hercules was an Excel nerd). And even the best projections can’t account for the unpredictability of an NFL season.

VBD also leaves out a lot of the nuance required to build a balanced team, and mostly ignores ADP in calculating “value.” VBD is a useful concept despite these flaws. It serves as just one of many ways you should be preparing for your draft.

## [Calculating VBD using VORP](https://www.fantasypros.com/2017/06/what-is-value-based-drafting/)
You generate VBD rankings by creating projections for every player, setting a baseline at each position, then calculating the difference between the two for each player.

For example, [insert RB] is projected to score 289.8 fantasy points. A standard 12 team league has 180 players drafted, and [the consensus ADP](https://www.fantasypros.com/nfl/adp/qb.php) shows X running backs being drafted in the top 180. That makes the (X+1)th running back, [insert RB] and his projected 67.1 fantasy points, the baseline for running backs using a VORP calculation. [first RB]’s VORP—his projected points minus [second RB]’s projected points—ends up a whopping 222.7.

## Usage

You must have [Python 3](https://www.python.org/downloads/), [pandas](https://pandas.pydata.org/pandas-docs/stable/install.html), and [numpy](https://scipy.org/install.html) installed.  

You must also have your data saved as a csv from http://apps.fantasyfootballanalytics.net/projections/, where you can use their standard
projections or enter your league's settings to get more accurate results for your draft.

In the command line enter:  
```python vbd.py [league_size] [team_size] [data_file]``` or ```./vbd.py [draft_size] [data_file]```, where:
* league_size is the number of teams in your league
* team_size is the number of players on each team
* data_file is the CSV file with the projections

You will then be prompted with 5 options: remove, adjust, draft, display, exit

### Remove
```remove [Player Name]``` or ```r [Player Name]```  
The name must be exactly as it is in the data, with proper capitalization. For defense's with only one word in the name you must add a space after name. The player will then be removed and will no longer show up in the "draft" or "display" commands
Note: Currently doesn't support players with the exact same name

### Adjust
```adjust [position] [multiplier]``` or ```a [position] [multiplier]```  
The position must be one of QB, RB, WR, TE, DST, or K. The VBD of all the players with the given position will be multiplied by the
multiplier and the players are resorted to reflect the change.

Sample Multiplier Matrix:

| Have            | Start 1 | Start 2 | Start 3 | Start 4 | Start 5+ |
|-----------------|---------|---------|---------|---------|----------|
| 0 of a position | 1.0     | 1.0     | 1.0     | 1.0     | 1.0      |
| 1 of a position | 0.8     | 1.0     | 1.0     | 1.0     | 1.0      |
| 2 of a position | 0.6     | 0.8     | 1.0     | 1.0     | 1.0      |
| 3 of a position | 0.4     | 0.6     | 0.8     | 1.0     | 1.0      |
| 4 of a position | 0.2     | 0.4     | 0.6     | 0.8     | 1.0      |

https://www.footballguys.com/05vbdrevisited.htm

### Draft
```draft [position]``` or ```dr [position]```  
The position must be one of ANY, QB, RB, WR, TE, DST, or K. You will be given the best available player (assuming you are removing players)
based on VBD

### Display
```display [position]``` or ```di [position]```  
The position must be one of ALL, QB, RB, WR, TE, DST, or K. You will be given the 10 best available players (assuming you are removing players)
based on VBD

### Exit
```exit``` or ```e```  
The program will stop running

### Output
The program produces two files, "original.csv" and "updated.csv". original.csv is a condensed version the original input file with a column for VBD.
updated.csv is the same as original.csv but is updated everytime you remove a player.
