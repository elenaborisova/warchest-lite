import collections
import random

import sqlite3

from game.board import Board
from game.player import Player
from game.action import Action
from game.unit import Unit


class Game:
    UNIT_TYPES = ()
    UNIT_COUNT = 4
    ACTIONS = {
        'place': Action.place,
        'control': Action.control,
        'move': Action.move,
        'recruit': Action.recruit,
        'attack': Action.attack,
        'initiative': Action.initiative,
    }
    ACTION_COUNT = 3
    HAND_UNIT_COUNT = 3

    def setup(self):
        # Connect to DB
        conn = sqlite3.connect('identifier.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name, win_count date FROM players ORDER BY date DESC")
        record = cursor.fetchall()
        print('Player win statistics:')
        [print(' -> '.join(map(str, r))) for r in record]
        print()
        cursor.close()

        # Create players
        crow_player = Player('Crow')
        crow_player.control_zones.append([0, 2])
        wolf_player = Player('Wolf')
        wolf_player.control_zones.append([4, 2])

        # Create board
        board = Board()
        board.mark_control_zone(crow_player)
        board.mark_control_zone(wolf_player)
        board.mark_free_zones()
        print(board)

        # Create 4 units
        Game.UNIT_TYPES = (Unit(name='Knight', count=5, attack_space=1, move_space=1),
                           Unit(name='Crossbowman', count=5, attack_space=2, move_space=1),
                           Unit(name='Mercenary', count=5, attack_space=1, move_space=1),
                           Unit(name='Archer', count=4, attack_space=2, move_space=1))

        # Randomly choose a player
        turns = Game.__randomly_choose_player(crow_player, wolf_player)

        # Randomly distribute unit types in bags
        Game.__randomly_generate_bags(crow_player, wolf_player)

        return turns, board

    def start_game(self, turns, board):
        user_input = input('Start game (y/n): ')
        while user_input not in ('y', 'n'):
            user_input = input('Start game (y/n): ')
        if user_input.lower() == 'n':
            exit()

        while True:
            player = turns[0]
            opponent = turns[1]
            Game.__randomly_generate_hand(player)
            print(player)

            for _ in range(Game.ACTION_COUNT):

                action = input('Choose an action (place, control, move, recruit, attack, initiative): ')
                while action not in Game.ACTIONS:
                    action = input('Choose an action (place, control, move, recruit, attack, initiative): ')

                if action in ('place', 'move'):
                    Game.ACTIONS[action](player, board)
                elif action in ('control', 'attack'):
                    Game.ACTIONS[action](player, opponent, board)
                else:
                    Game.ACTIONS[action](player)

                Game.__check_if_player_wins(player, opponent)
                print(board)
                print(f'Hand: {", ".join(player.hand)}')

            if not player.initiative:
                turns.append(turns.popleft())
            else:
                player.initiative = False

    @staticmethod
    def __randomly_generate_hand(player):
        if len(player.bag) < Game.HAND_UNIT_COUNT:
            Game.__fill_player_bag(player)

        random_sample = random.sample(player.bag, Game.HAND_UNIT_COUNT)
        for unit in random_sample:
            player.hand.append(unit)
            player.bag.remove(unit)

    @staticmethod
    def __fill_player_bag(player):
        player.bag.extend(player.discarded_units)
        player.discarded_units = []

    @staticmethod
    def __randomly_choose_player(player1, player2):
        return collections.deque(random.sample([player1, player2], 2))

    @staticmethod
    def __randomly_generate_bags(player1, player2):
        random_sample = random.sample(range(Game.UNIT_COUNT), Player.UNIT_COUNT)

        for i in range(len(Game.UNIT_TYPES)):
            if i in random_sample:
                [player1.bag.append(Game.UNIT_TYPES[i].name) for _ in range(Player.UNIT_COUNT)]
                player1.recruitment_pieces[Game.UNIT_TYPES[i].name] = Game.UNIT_TYPES[i].count - 2
            else:
                [player2.bag.append(Game.UNIT_TYPES[i].name) for _ in range(Player.UNIT_COUNT)]
                player2.recruitment_pieces[Game.UNIT_TYPES[i].name] = Game.UNIT_TYPES[i].count - 2

    @staticmethod
    def __check_if_player_wins(player, opponent):
        if player.control_tokens == 0 or \
                (not opponent.bag and not opponent.hand
                 and not opponent.units_on_board and not opponent.recruitment_pieces):
            print(f'{player.name} IS THE WINNER!!!')
            exit()


if __name__ == '__main__':
    game = Game()
    turns, board = game.setup()
    game.start_game(turns, board)
