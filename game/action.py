from player import Player
from board import Board


class Action:
    UNIT_TYPES = ("Archer", "Berserker", "Cavalry", "Knight")

    @staticmethod
    def place(player: Player, board: Board):
        unit = input('Which unit from your hand would you like to place? ')
        while unit not in Action.UNIT_TYPES or unit not in player.hand:
            unit = input('Invalid unit. Which unit from your hand would you like to place? ')

        position = list(map(int, input(f'Where would you like to place {unit}? ').split(',')))
        #ToDo: check if position is valid (Orthogonally adjacent and in bounds)

        player.hand.remove(unit)
        board.board[position[0]][position[1]] = unit[0]
        player.units_on_board.add(unit)

    @staticmethod
    def control(player: Player):
        pass

    @staticmethod
    def move(player: Player, board: Board):
        from_position = list(map(int, input('From position (row, col): ').split(',')))  # ToDo: check if valid

        unit = input('Which unit from your hand would you like to move? ')
        while unit not in Action.UNIT_TYPES or unit not in player.hand \
                or unit not in player.units_on_board:
            unit = input('Invalid unit. Which unit from your hand would you like to move? ')

        to_position = list(map(int, input('To position (row, col): ')))  # ToDo: check if valid

        board.board[from_position[0]][from_position[1]] = '.'
        board.board[to_position[0]][to_position[1]] = unit[0]

        player.hand.remove(unit)

    @staticmethod
    def recruit(player: Player):
        unit = input('Which unit would you like to discard from your hand to recruit the same kind? ')
        while unit not in Action.UNIT_TYPES or unit not in player.hand:
            unit = input('Invalid unit. Which unit would you like to discard from your hand to recruit the same kind? ')

        player.hand.remove(unit)
        player.bag.append(unit)
        player.discarded_units.append(unit)
        player.recruitment_pieces[unit] -= 1

        print(f'{unit} discarded from hand and added to bag.\n')

    @staticmethod
    def attack(player: Player):
        pass

    @staticmethod
    def initiative(player: Player):
        unit = input('Which unit would you like to discard from your hand? ')
        while unit not in Action.UNIT_TYPES or unit not in player.hand:
            unit = input('Invalid unit. Which unit would you like to discard from your hand? ')

        player.hand.remove(unit)
        player.discarded_units.append(unit)

        print(f'{unit} discarded from hand.\n')

