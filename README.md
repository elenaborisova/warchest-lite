## Warchest Lite :rocket:

A console game as a simplified version of the board game _Warchest Lite_
> Creator: @elenaborisova :girl:  
> Language: Python :snake:

## Rules of the game

Warchest is a game about controlling zones and making strategies. The original game is played with a 9x9 board with 9
types of pieces, and the goal of the game is for a player to have 6 controlled zones before their opponent. To do so,
the player will place and move units and attack their opponent’s units.

## Assumptions

**Board size:** 5x5  
**Players:** 2  
**Units:** 4 units (2 per player)  
**Player hand count:** 3  
**Player bag count:** 4 (2 unit types x 2 each)  
**Free zones:** 4  
**Player's control zones at the beginning of the game:** 1 per player  
**Player's control tokens for the win:** 3

## Main classes

### Board

Class Board represents the 5x5 matrix board where the game will be played.

It contains class variables "SIZE", "FREE_ZONE_SYMBOL", "FREE_ZONE_POSITIONS" as these are constants that are shared
between any instance of this class. When a new board is created (an instance of the class Board), it is initialized with
an empty (".") 5x5 matrix.

It has the only property board which is encapsulated and has its own getters and setters.

The class contains two methods that place specific "items" on the board:

- To mark control zones (used when starting the game to mark the positions of the two players)
- To mark free zones (used when starting the game to mark the positions of the free zones ("@"))

The board class also has a magic method used to represent the matrix in a visual way, by adding headers on the top and
left side.

### Player

The Player class is used to represent a player of the game.

Every player (no matter the instance) shares some common variables - "BAG_SIZE" and "UNIT_COUNT".

Each individual player has the following properties (that are encapsulated and have getters and setters created):

- name - in this instance of the game, could be either "Wolf" or "Crow"
- control zones - an empty list - initially only the zones they occupy ([4 ,2], [0, 2]) - it is expected to be able to
  add to this list more control zones
- bag - initially an empty list - it will be filled by randomly choosing 2 units and placing 2 of each type in the bag
- hand - empty list - each round the hand will be filled with randomly generated 3 units from the bag
- recruitment pieces - a dictionary - would be populated with the items in the bag and their corresponding total unit
  count
- discarded units pile - a list that would contain any item the player decides to discard during the game actions
- control tokens - count of 3 - the needed control zones the player should conquer in order to win the game
- units on board - a set containing the name of the units a player has on board - used to quickly (O(1) time) validate
  whether the user has requested items on board
- initiative - a boolean - initially False - which would change with the "initiative" action and would signal whether
  the player will repeat their turn in the next round

The player has one magic representation method used to help visualize the status of player's possession before each new
round.

### Unit

The Unit class represents a unit type that has its own specific name, total unit count, attack space, and move space.

These properties are encapsulated and validated for Value Errors in their respective setters.

The Unit class has a static method that checks whether a unit can be moved/placed/attacked from a particular position.
The method is currently implemented as generic (static and irrespective of specific unit implementation) as it checks
only for adjacent positions with 1 space difference. This is a potential improvement of the method, which could use the
specific move and attack space counts of each unit type.

### Action

The Action Class is the most logic intensive one. It consists of 6 static methods that represent an action and 5 more
private helper methods. All methods implemented are static as we do not need a specific instance of the Action class in
order to use those methods in the main game logic.

#### *Recruit action*

First, the user is asked to input a unit name that they want to recruit. The private helper method checks whether this
unit is one of the 4 available (in the class constant variable) and whether the user has this unit in their hand.  
The user is prompted to type a correct name several times.

If the unit name is correct, but there are no more units of this type to recruit, the user will get a "Failed action"
message and continue with the next action/round.

If the checks pass, the unit will be removed from the player's hand, placed in their discarded units pile, lowered the
count of this recruitment piece, and finally appended to their bag.  
The player will get a "Success" message.

#### *Initiative action*

The user is asked for a unit name to discard in orderded to get the initiative for next round. They are prompted
repeatedly for correct input.

The unit name is removed from the player's hand, put into the discarded items pile, and the boolean "initiative" is set
to True.

Finally, a "Success" message is displayed.

#### *Place action*

First, there is a check to verify whether the player can place any units. If the player does not have any control zones,
they cannot place an unit. In this case, an "Invalid" message is displayed to the player and the game continues for the
next action/round.

Then, the player is asked to input the unit name of the unit they want to place, and the position (row,col) where they
want to place it. Both inputs are checked and validated for correct unit name and in bounds position. The user is
prompted until they type the correct values.

Then, the position is verified one more time of whether it is adjacent to a control zone of the player or not. If not,
the action terminates and a "Invalid action" message is displayed for the player.

If all the checks pass, the unit is removed from hand and placed on board.

#### *Move action*

The player is prompted for unit name and position to and from where to move this unit.

If the unit name is valid, but is not on board, the action terminates. If the "from position" is in bounds but do not
correspond to the unit name, the action terminates. If the "to position" is in bounds but not adjacent to the "from
position", the action terminates.

If all the checks pass, the unit is moved from one position to the other, the unit is removed from hand and added to
discard pile.

#### *Control action*

The player is asked for valid unit name and position to control on the board.

If both values are valid, there is another check that verifies whether the position the player wants to control is
either a free zone ("@") or opponent controlled zone. Also, the player cannot control its own control zones.

If successful, the unit is removed from hand, added to discard pile, marked on the board. Position is added to control
positions of the player and the control tokens are reduced by 1.

#### *Attack action*

The player is asked for unit name (from their own hand and on board) and opponent's unit name to attack. Both are
verified.

Then the player is prompted to provide a "from" and "to" position coordinates on the board, showing where those two
units are located. The positions are also verified to be in bounds and correspond to unit names. The second position is
also checked for adjacency with the first.

If all the checks pass, the unit is removed from hand and discarded. The board is marked with the new unit symbol.

Finally, the opponent's unit is deleted from the game - from all properties that might contain the unit.

### Game

This is where the main game logic is.

The game class has several class variables, a "setup" and "start game" methods and several private helper methods.

Before the game has started, we go through a setup - initialize the two players with their corresponding control zones,
initialize the board and mark the two players' control zones and free zones on it. Then, create the 4 unit types. Use
the helper method to randomly choose the turns of players and randomly distribute the 4 units amongst them (in their
bags).

When the game starts, we create sets of 3 actions per round. In each round, we pick a player (by their turns) and randomly generate their hand from their bag of units. 

We ask the user to choose an action, and depending on the action chosen, call the corresponding action method.

After each action, we check whether the player has won the game or not.  
After each round, we check who has the initiative and determine the turn for the next round.

The game continues until one player wins.

## Requirements checklist

- [ ] README in English
- [ ] Minimum 4 unit types
- [ ] Actions implemented: initiative, move, attack (+deletion), recruit, place
- [ ] Winning conditions
- [ ] GitHub repo with PRs
- [ ] Unit tests
- [ ] Object Oriented Design
- [ ] Documentation
- [ ] Create SQLite database with player data