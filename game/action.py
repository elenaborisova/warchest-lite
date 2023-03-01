from game.unit import Unit


class Action:
    UNIT_TYPES = ('Knight', 'Crossbowman', 'Mercenary', 'Archer')

    @staticmethod
    def place(player, board):
        if not player.control_zones:
            print('Not permitted. You do not have any control zones. Try again in the next round!')
            return

        unit = Action.__prompt_user_for_unit_name('Which unit would you like to place? ', player)
        row, col = Action.__prompt_user_for_position(f'Where would you like to place {unit} (row,col)? ', board)

        if not Unit.can_move_to_pos(player.control_zones, [row, col]):
            print(f'Not permitted. You cannot place {unit} in an non-adjacent zone. Try again in the next round!')
            return

        player.hand.remove(unit)
        board.board[row][col] = unit[0]
        player.units_on_board.add(unit)

    @staticmethod
    def control(player, opponent, board):
        unit = Action.__prompt_user_for_unit_name('Which unit would you like to discard for control? ', player)

        row, col = Action.__prompt_user_for_position('Which position would you like to control (row,col)? ', board)

        if not (board.board[row][col] == board.FREE_ZONE_SYMBOL or [row, col] in opponent.control_zones) \
                or [row, col] in player.control_zones:
            print(f'Not permitted. This zone as is neither free nor opponent-controlled. Try again in the next round!')
            return

        player.hand.remove(unit)
        player.discarded_units.append(unit)
        board.board[row][col] = unit[0]
        player.control_tokens -= 1
        player.control_zones.append([row, col])
        player.units_on_board.add(unit)

    @staticmethod
    def move(player, board):
        unit = Action.__prompt_user_for_unit_name('Which unit would you like to move? ', player)
        if unit not in player.units_on_board:
            print(f'Not permitted. {unit} is not on your board. Try again in the next round!')
            return

        from_row, from_col = Action.__prompt_user_for_position('Move from position (row, col): ', board)
        if not board.board[from_row][from_col] == unit[0]:
            print(f'Not permitted. {unit} is not on this position. Try again in the next round!')
            return

        to_row, to_col = Action.__prompt_user_for_position('Move to position (row, col): ', board)
        if not Unit.can_move_to_pos([[from_row, from_col]], [to_row, to_col]):
            print('Not permitted. You cannot move in an non-adjacent zone. Try again in the next round!')
            return

        board.board[from_row][from_col] = '.'
        board.board[to_row][to_col] = unit[0]
        player.hand.remove(unit)
        player.discarded_units.append(unit)

    @staticmethod
    def recruit(player):
        unit = Action.__prompt_user_for_unit_name('Which unit would you like to recruit? ', player)

        if player.recruitment_pieces[unit] <= 0:
            print(f'Not permitted. You don\'t have more units of type {unit} to recruit. Try again in the next round!')
            return

        player.hand.remove(unit)
        player.discarded_units.append(unit)
        player.bag.append(unit)
        player.recruitment_pieces[unit] -= 1

        print(f'{unit} successfully discarded from hand and added to bag!\n')

    @staticmethod
    def attack(player, opponent, board):
        unit = Action.__prompt_user_for_unit_name('Which unit would you like to use for attack? ', player)
        if unit not in player.units_on_board:
            print(f'Not permitted. {unit} is not on your board. Try again in the next round!')
            return

        unit_to_attack = Action.__prompt_user_for_unit_name('Which opponent unit would you like to attack? ', opponent)
        if unit_to_attack not in opponent.units_on_board:
            print(f'Not permitted. {unit} is not on your opponent\'s board. Try again in the next round!')
            return

        from_row, from_col = Action.__prompt_user_for_position('Attack from position (row,col): ', board)
        if not board.board[from_row][from_col] == unit[0]:
            print(f'Not permitted. {unit} is not on this position. Try again in the next round!')
            return

        to_row, to_col = Action.__prompt_user_for_position('Position to attack (row,col): ', board)
        if not board.board[to_row][to_col] == unit_to_attack[0]:
            print(f'Not permitted. {unit} is not on this position. Try again in the next round!')
            return
        if not Unit.can_move_to_pos([[from_row, from_col]], [to_row, to_col]):
            print(f'Not permitted. You cannot attack an non-adjacent zone. Try again in the next round!')
            return

        player.hand.remove(unit)
        player.discarded_units.append(unit)
        board.board[from_row][from_col] = '.'
        board.board[to_row][to_col] = unit[0]

        Action.__delete_attacked_unit(opponent, unit_to_attack)
        if [from_row, from_col] in opponent.control_zones:
            opponent.control_zones.remove([from_row, from_col])

    @staticmethod
    def initiative(player):
        unit = Action.__prompt_user_for_unit_name('Which unit would you like to discard from your hand? ', player)

        player.hand.remove(unit)
        player.discarded_units.append(unit)
        player.initiative = True

        print(f'{unit} successfully discarded from hand! You have the initiative for next round!\n')

    @staticmethod
    def __delete_attacked_unit(player, unit):
        player.units_on_board.remove(unit)
        player.recruitment_pieces.pop(unit)

        while unit in player.hand:
            player.hand.remove(unit)

        while unit in player.bag:
            player.bag.remove(unit)

        while unit in player.discarded_units:
            player.discarded_units.remove(unit)

    @staticmethod
    def __is_position_valid(row, col, size):
        return 0 <= row < size and 0 <= col < size

    @staticmethod
    def __is_unit_valid(unit, player):
        return unit in Action.UNIT_TYPES and unit in player.hand

    @staticmethod
    def __prompt_user_for_unit_name(message, player):
        unit = input(message)
        while not Action.__is_unit_valid(unit, player):
            unit = input('Invalid unit. ' + message)

        return unit

    @staticmethod
    def __prompt_user_for_position(message, board):
        row, col = list(map(int, input(message).split(',')))
        while not Action.__is_position_valid(row, col, board.SIZE):
            row, col = list(map(int, input('Invalid position. ' + message).split(',')))

        return row, col
