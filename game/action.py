from player import Player
from board import Board


class Action:
    UNIT_TYPES = ("Archer", "Berserker", "Cavalry", "Knight")

    @staticmethod
    def place(player: Player, board: Board):
        if not player.control_zones:
            print('You can\'t place a unit as you do not have any control zones.')
            return

        unit = input('Which unit from your hand would you like to place? ')
        while unit not in Action.UNIT_TYPES or unit not in player.hand:
            unit = input('Invalid unit. Which unit from your hand would you like to place? ')

        row, col = list(map(int, input(f'Where would you like to place {unit} (row,col)? ').split(',')))
        # ToDo: check if position is valid (Orthogonally adjacent to control zone and in bounds)

        player.hand.remove(unit)
        board.board[row][col] = unit[0]
        player.units_on_board.add(unit)

    @staticmethod
    def control(player: Player, opponent: Player, board: Board):
        unit = input('Which unit from your hand would you like to discard? ')
        while unit not in Action.UNIT_TYPES or unit not in player.hand:
            unit = input('Invalid unit. Which unit from your hand would you like to discard? ')

        row, col = list(map(int, input(f'Which position would you like {unit} to control (row,col)? ').split(',')))
        # ToDo: check if position is valid (Orthogonally adjacent to control zone and in bounds, unit specific)

        if not (board.board[row][col] == Board.FREE_ZONE_SYMBOL or [row, col] in opponent.control_zones) \
                or [row, col] in player.control_zones:
            print('Invalid position.')
            return

        player.hand.remove(unit)
        player.discarded_units.append(unit)
        board.board[row][col] = unit[0]
        player.control_tokens -= 1
        player.control_zones.append([row, col])
        player.units_on_board.add(unit)

    @staticmethod
    def move(player: Player, board: Board):
        unit = input('Which unit from your hand and on the board would you like to move? ')
        while unit not in Action.UNIT_TYPES or unit not in player.hand \
                or unit not in player.units_on_board:
            unit = input('Invalid unit. Which unit from your hand and on the board would you like to move? ')

        from_row, from_col = list(map(int, input('From position (row, col): ').split(',')))  # ToDo: check if valid
        to_row, to_col = list(map(int, input('To position (row, col): ').split(',')))  # ToDo: check if valid and orthogonal

        board.board[from_row][from_col] = '.'
        board.board[to_row][to_col] = unit[0]

        player.hand.remove(unit)
        player.discarded_units.append(unit)

    @staticmethod
    def recruit(player: Player):
        unit = input('Which unit would you like to discard from your hand to recruit the same kind? ')
        while unit not in Action.UNIT_TYPES or unit not in player.hand:
            unit = input('Invalid unit. Which unit would you like to discard from your hand to recruit the same kind? ')

        if player.recruitment_pieces[unit] <= 0:
            print(f'You don\'t have more units of type {unit} to recruit.')
            return

        player.hand.remove(unit)
        player.discarded_units.append(unit)
        player.bag.append(unit)
        player.recruitment_pieces[unit] -= 1

        print(f'{unit} successfully discarded from hand and added to bag!\n')

    @staticmethod
    def attack(player: Player, opponent: Player, board: Board):
        unit = input('Which unit from your hand and on the board would you like to use for attack? ')
        while unit not in Action.UNIT_TYPES or unit not in player.hand \
                or unit not in player.units_on_board:
            unit = input('Invalid unit. Which unit from your hand and on the board would you like to use for attack? ')

        unit_to_attack = input('Which opponent\'s unit on the board would you like to attack? ')
        while unit_to_attack not in Action.UNIT_TYPES or unit_to_attack not in opponent.units_on_board:
            unit_to_attack = input('Invalid unit. Which opponent\'s unit on the board would you like to attack? ')

        row, col = list(map(int, input(f'Which position would you like {unit} to attack (row,col)? ').split(',')))
        # ToDo: check if position is valid (Orthogonally adjacent to control zone and in bounds, unit specific)

        if not [row, col] in opponent.control_zones:
            print('Invalid position.')
            return

        player.hand.remove(unit)
        player.discarded_units.append(unit)
        board.board[row][col] = unit[0]

        Action.__delete_attacked_unit(opponent, unit_to_attack)

    @staticmethod
    def initiative(player: Player):
        unit = input('Which unit would you like to discard from your hand? ')
        while unit not in Action.UNIT_TYPES or unit not in player.hand:
            unit = input('Invalid unit. Which unit would you like to discard from your hand? ')

        player.hand.remove(unit)
        player.discarded_units.append(unit)
        player.initiative = True

        print(f'{unit} successfully discarded from hand! You have the initiative for next round!\n')

    @staticmethod
    def __delete_attacked_unit(player: Player, unit):
        player.units_on_board.remove(unit)
        player.recruitment_pieces.pop(unit)
        player.bag.remove(unit)
        player.discarded_units.remove(unit)
        player.hand.remove(unit)
