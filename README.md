# A Random Game
* This is a game I have been working on both as a school and independent project, with some help from friends about what I should add.
* I am a very inexperienced coder, so many parts of this may very well be excessively bulky, redundant, etc.
* This game is meant to be run through Python 3; I use Python 3.7.1 at school and 3.6.2 at home (due to inability to update at home).
* Bugs, Questions, Suggestions & Comments: Contact me at quasistellarobst@gmail.com

## Game Play
### Overview
ARandomGame is a turn-based game in which the player collects resources and... well, that's about it right now. I'm still working on features like buildings and objectives. Anyways, you can collect Food, Wood, and Iron, and you have to maintain your population as you go along! (Not very hard to do right now—I'm working on that too).
### Map & Resources
* Click on a tile to place or remove a worker.
* Click the **End Turn** button at the bottom to end the turn, naturally.
* You cannot place workers on unrevealed tiles.
* Map tiles may be revealed at the end of a turn if there is a worker placed in a 1-square radius (*i.e.*, in one of the 8 adjacent tiles). Each square has a separate 50% chance to be revealed, which will stack with other tiles (so if an unrevealed tile is bordering 2 occupied tiles, there is a 75% chance of it being revealed).
* When a turn ends, if you have more workers placed than you have people, workers will be removed. This happens **BEFORE** birth rate!
* Workers on tiles that do not produce food will be removed first.
* Workers are removed starting from the top left corner, clearing a row before moving to the next.
#### Food
* Tiles yield 1-3 Food randomly.
* You need 1 Food per Population unit.
* Currently, food is stored in three "groups": Turn 1, Turn 2, and Turn 3. To simulate food spoiling, the oldest food group is removed at the end of each turn, and a new group is created with any food from that turn.
  * Granaries add new groups when active.
#### Wood
* Tiles yield 1-3 Wood randomly.
* Buildings require wood to be built; the more buildings of one kind, the more it will cost.
#### Iron
* Tiles yield 1-2 Iron randomly.
* Buildings require iron to be built; the more buildings of one kind, the more it will cost.
#### Gold
* You cannot currently find Gold naturally.
* You can trade Food, Wood, or Iron for Gold.
* Buildings require gold to be built; the required Gold increases both with turn (inflation) and quantity of that building type.
### Population Growth
* At the moment, you gain *n* Population per turn where *n* is that largest integer value that satisfies:
  * Excess Food ≥ (2*n*³+3*n*²+25*n*)/6
* The death rate varies from 10-35% and is independently random per turn.
* There is a 0.01% chance of a mass dying event in which the death rate will be 91%.
### Trade
* You can trade Food, Wood, Iron, and Gold here. If we determine a base unit as @1, the resources have the following values:
  * Food: @1
  * Wood: @2
  * Iron: @5
  * Gold: @100
* There is a 10% deduction of the material you receive.
  * For example, if you trade Gold for Food, you will receive 90 Food per Gold rather than 100 Food as the key above might suggest.
* The trade value isn't exact; rather, it has a deviation of up to 10%. (It used to have a deviation of ±5 units of the request material, but the new system is less rewarding of small trades and much more rewarding for large trades.)
  * For example, if you trade 1 Gold for Food, you can receive 81-99 food (90±10%).
* The `Auto-Reset` toggle is for automatically resetting the trade panel at the end of a turn. By default, it is on (*i.e.*, it will reset).
* The `Reset` button allows you to immediately reset the trade panel.
* The `Show conversion rates` button will display how much of each resource can be traded for with the current Trade input.
  * For example, if you select "Trade: Gold" from the first dropdown and type "1" under that, it will show:
    * Food: 81-99
    * Wood: 40-49
    * Iron: 16-19
    * Gold: 0-0
  * The last one is not a bug; remember that 10% of the value is deducted. The 10% deviation is of the new value—so the maximum is 0.99, which is floored to 0.
* The calculations do not automatically update. They will update when you click the `Refresh` button.
### Buildings
* You can build Granaries, Sawmills, and Mines. They boost your respective abilities to gain Food, Wood, and Iron.
* Granaries add an extra "turn" to your food list; in other words, it takes an extra turn before your food spoils.
* Sawmills can modify a Wood tile currently yielding less than 3 Wood (the top number plus the bottom modifier). Each sawmill yields +1 Wood.
* Mines do the same as Sawmills, except for Iron.
* You place Sawmills and Mines on tiles using the `Place building` button and remove them with the `Remove building` button.
### Save
* This is a feature I entrust you as the user to use appropriately. It imports Python files and takes the variables, rather than reading a file.
  * This makes the feature rather exploitable, as you can launch Python programs within this program. However, you could do it without the program, so I'm not all too concerned.
* The save files are intentionally not encrypted. This allows for easy editing so that you can set custom start conditions, easily reproduce a bug, et cetera.
  * When a save file is loaded in, an indicator will appear in the game window saying 'Loaded File!' to indicate to others that a file was loaded in and may have been used to achieve certain things.
* You only need to specify the name when Saving or Loading a file; it is automatically assumed to be in the same folder as the program itself.
