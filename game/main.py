import collections
import random

from board import Board
from player import Player
from action import Action


def setup():
    # Setup
    UNIT_TYPES = ("Archer", "Berserker", "Cavalry", "Crossbowman")

    crow_player = Player("Crow")
    crow_player.control_zones.append([0, 2])
    wolf_player = Player("Wolf")
    wolf_player.control_zones.append([4, 2])

    game_board = Board()
    game_board.mark_control_zone(crow_player)
    game_board.mark_control_zone(wolf_player)
    game_board.mark_free_zones()

    print(game_board)

    # Randomly choose a player
    turns = collections.deque()
    current_player = random.choice([crow_player, wolf_player])
    if current_player == crow_player:
        turns.append(crow_player)
        turns.append(wolf_player)
    else:
        turns.append(wolf_player)
        turns.append(crow_player)

    # Randomly distribute unit types in bag
    random_sample = random.sample(range(0, 4), 2)
    for i in range(len(UNIT_TYPES)):
        if i in random_sample:
            [crow_player.bag.append(UNIT_TYPES[i]) for _ in range(2)]
            crow_player.recruitment_pieces[UNIT_TYPES[i]] = 4  #ToDo: find where this number comes from
        else:
            [wolf_player.bag.append(UNIT_TYPES[i]) for _ in range(2)]
            wolf_player.recruitment_pieces[UNIT_TYPES[i]] = 4

    # Randomly distribute unit types in hand
    random_sample = random.sample(range(len(crow_player.bag)), 3)
    for i in random_sample:
        crow_player.hand.append(crow_player.bag[i])
        wolf_player.hand.append(wolf_player.bag[i])

    print(current_player)
    return turns


def start_game():
    user_input = input('Start game (y/n): ')
    while user_input not in ('y', 'n'):
        user_input = input('Start game (y/n): ')

    if user_input.lower() == 'n':
        exit()

    turns = setup()
    player = turns[0]
    is_order_changed = False

    UNIT_TYPES = ("Archer", "Berserker", "Cavalry", "Crossbowman")
    ACTIONS = {
        'place': Action.place,
        'control': Action.control,
        'move': Action.move,
        'recruit': Action.recruit,
        'attack': Action.attack,
        'initiative': Action.initiative,
    }

    while True:
        action = input('Choose an action (place, control, move, recruit, attack, initiative): ')
        while action not in ACTIONS:
            action = input('Choose an action (place, control, move, recruit, attack, initiative): ')

        ACTIONS[action](player)

        if action == 'initiative':
            is_order_changed = True
        if not is_order_changed:
            turns.append(turns.popleft())
            player = turns[0]
            is_order_changed = False


if __name__ == '__main__':
    start_game()
