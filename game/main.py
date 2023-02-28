import collections
import random

from board import Board
from player import Player
from action import Action


class Game:
    UNIT_TYPES = ("Archer", "Berserker", "Cavalry", "Knight")
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
        # Create players
        crow_player = Player("Crow")
        crow_player.control_zones.append([0, 2])
        wolf_player = Player("Wolf")
        wolf_player.control_zones.append([4, 2])

        # Create board
        board = Board()
        board.mark_control_zone(crow_player)
        board.mark_control_zone(wolf_player)
        board.mark_free_zones()
        print(board)

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
            Game.__randomly_generate_hand(opponent)
            print(player)

            for _ in range(Game.ACTION_COUNT):

                action = input('Choose an action (place, control, move, recruit, attack, initiative): ')
                while action not in Game.ACTIONS:
                    action = input('Choose an action (place, control, move, recruit, attack, initiative): ')

                if action in ('place', 'move'):
                    Game.ACTIONS[action](player, board)
                elif action == 'control':
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
        if not player.bag:
            Game.__fill_player_bag(player)

        random_sample = random.sample(range(Player.BAG_SIZE), Game.HAND_UNIT_COUNT)
        for i in random_sample:
            player.hand.append(player.bag[i])

    @staticmethod
    def __fill_player_bag(player):
        player.bag = player.discarded_units
        player.discarded_units = []

    @staticmethod
    def __randomly_choose_player(player1, player2):
        turns = collections.deque()
        current_player = random.choice([player1, player2])

        if current_player == player1:
            turns.append(player1)
            turns.append(player2)
        else:
            turns.append(player2)
            turns.append(player1)

        return turns

    @staticmethod
    def __randomly_generate_bags(player1, player2):
        random_sample = random.sample(range(Game.UNIT_COUNT), Player.UNIT_COUNT)

        for i in range(len(Game.UNIT_TYPES)):
            if i in random_sample:
                [player1.bag.append(Game.UNIT_TYPES[i]) for _ in range(Player.UNIT_COUNT)]
                player1.recruitment_pieces[Game.UNIT_TYPES[i]] = 4  # ToDo: find where this number comes from
            else:
                [player2.bag.append(Game.UNIT_TYPES[i]) for _ in range(Player.UNIT_COUNT)]
                player2.recruitment_pieces[Game.UNIT_TYPES[i]] = 4

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
