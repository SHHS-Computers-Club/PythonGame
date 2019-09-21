# A Random Game
* This game is meant to be run through Python 3; development occurs on multiple versions (including at least 3.7.1 and 3.6.2)
* Bugs, Questions, Suggestions & Comments: quasistellarobst@gmail.com

## Game Play
### Overview
PythonGame is a turn-based game in which the player collects resources and... well, that's about it right now. Features like buildings and objectives are currently in development. Anyways, you can collect Food, Wood, and Iron, and you have to maintain your population as you go along! (Not very hard to do right now—balance is also being refined).
### Map & Resources
* Click on a tile to place or remove a worker.
* Click the **End Turn** button at the bottom to end the turn.
* You cannot place workers on unrevealed tiles.
* Map tiles may be revealed at the end of a turn if there is a worker placed in a 1-square radius (*i.e.*, in one of the 8 adjacent tiles). Each square has a separate 50% chance to be revealed, which will stack with other tiles (so if an unrevealed tile is bordering 2 occupied tiles, there is a 75% chance of it being revealed).
* When a turn ends, if you have more workers placed than you have people, workers will be removed. This happens **BEFORE** birth rate!
* Workers on tiles that do not produce food will be removed first.
* Workers are removed starting from the top left corner, clearing a row before moving to the next.
#### Food
* Tiles can yield 1-3 Food, determined at the start of the game randomly (with slight weighting).
* You need 1 Food per Population unit.
* Currently, food is stored in three "groups": Turn 1, Turn 2, and Turn 3. To simulate food spoiling, the oldest food group is removed at the end of each turn, and a new group is created with any food from that turn.
  * Granaries add new groups when active.
#### Wood
* Tiles can yield 1-3 Wood, determined at the start of the game randomly.
* Buildings require wood to be built; the more buildings of one kind, the more it will cost.
#### Iron
* Tiles can yield 1-2 Iron, determined at the start of the game randomly.
* Buildings require iron to be built; the more buildings of one kind, the more it will cost.
#### Gold
* You cannot currently find Gold naturally.
* You can trade Food, Wood, or Iron for Gold.
* Buildings require gold to be built; the required Gold increases both with turn (inflation) and quantity of that building type.
### Population Growth
* At the moment, you gain *n* Population per turn where *n* is that largest integer value that satisfies:
  * Excess Food ≥ (2*n*³+3*n*²+25*n*)/6
* The death rate varies from 10-35% and is independently random per turn.
* There is a 0.01% chance of a mass death in which the death rate will be 91%.
### Trade
* You can trade Food, Wood, Iron, and Gold here. With a base unit @1, the resources have the following values:
  * Food: @1
  * Wood: @2
  * Iron: @5
  * Gold: @20
* There is a 10% tax on the material you receive.
  * For example, if you trade Gold for Food, you will receive 18 Food per Gold rather than 20 Food as the key above might suggest.
* The trade value isn't exact; rather, it has a deviation of up to 10% (rounded down). (It used to have a deviation of ±5 units of the request material, but the new system is less rewarding of small trades and much more rewarding for large trades, in terms of potential efficiency.)
  * For example, if you trade 10 Gold for Food, you can receive 162-198 food (90±10%, which in this case is 180±18).
* The `Auto-Reset` toggle is for automatically resetting the trade panel at the end of a turn. By default, it is on (*i.e.*, it will reset).
* The `Reset` button allows you to immediately reset the trade panel.
* The `Show conversion rates` button will display how much of each resource can be traded for with the current Trade input.
  * For example, if you select "Trade: Gold" from the first dropdown and type "1" under that, it will show:
    * Food: 16-19
    * Wood: 8-9
    * Iron: 3-3
    * Gold: 0-0
  * The last one is not a bug; remember that 10% of the value is deducted. The 10% deviation is of the new value—so the maximum is 0.99, which is floored to 0.
* The calculations do not automatically update. They will update when you click the `Refresh` button.
### Buildings
* You can build Granaries, Sawmills, and Mines. They boost your respective abilities to gain (or store, in the former case) Food, Wood, and Iron.
* You can build a building by pressing the `Confirm Build` button, which should turn grey. If it is grey when you press `End Turn`, you will receive that building, provided you have the necessary materials.
* Granaries add an extra "turn" to your food list; in other words, it takes an extra turn before your food spoils.
* Sawmills can modify a Wood tile currently yielding less than 3 Wood (the top number plus the bottom modifier). Each sawmill yields +1 Wood.
* Mines do the same as Sawmills, except in that they apply to Iron instead of Wood (with the same limit of 3 per tile).
* Sawmills and Mines are placed on tiles using the `Place building` button and remove them with the `Remove building` button.
* Building prices become gradually higher in resources, each building (of a type) requiring in total:
  * The base price (300, 100, and 400 respectively) + 50 Wood per existing building of that type
  * The base price (150, 150, and 200 respectively) + 50 Iron per existing building of that type
  * 50 + 50 Gold per existing building of that type
    * Additional inflation rate of 4% per 100 turns, rounded down (price = int(50(*n*+1) * 1.04^(0.01*t*)) for *n* buildings and *t* turns)
### Save
* This is a feature I entrust you as the user to use appropriately. It imports Python files and takes the variables, rather than reading a regular text file.
  * This makes the feature rather exploitable, as you can launch Python programs within this program. However, you could do it without the program, so I'm not all too concerned.
* The save files are intentionally unencrypted. This allows for easy editing so that you can set custom start conditions, easily reproduce a bug, et cetera.
  * When a save file is loaded in, an indicator will appear in the game window saying 'Loaded File!' to indicate that a file was loaded in and may have been used to achieve certain things.
* You only need to specify the name when Saving or Loading a file; it is automatically assumed to be in the same folder as the program itself. (You also do not need the file extension, `.py`.)
