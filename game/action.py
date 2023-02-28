class Action:
    UNIT_TYPES = ('Knight', 'Crossbowman', 'Mercenary', 'Archer')

    @staticmethod
    def place(player, board):
        if not player.control_zones:
            print('You can\'t place a unit as you do not have any control zones.')
            return

        unit = Action.__prompt_user_for_unit_name('Which unit from your hand would you like to place? ', (), player)

        row, col = Action.__prompt_user_for_position(
            f'Where would you like to place {unit} (row,col)? ',
            (),
            board)
        # ToDo: are there other restrictions for placing the unit?

        player.hand.remove(unit)
        board.board[row][col] = unit[0]
        player.units_on_board.add(unit)

    @staticmethod
    def control(player, opponent, board):
        unit = Action.__prompt_user_for_unit_name('Which unit from your hand would you like to discard? ', (), player)

        row, col = Action.__prompt_user_for_position(
            f'Which position would you like {unit} to control (row,col)? ',
            (lambda row, col: (not (board.board[row][col] == board.FREE_ZONE_SYMBOL or
                                    [row, col] in opponent.control_zones) or [row, col] in player.control_zones)),
            board)
        # ToDo: check if unit can move there

        player.hand.remove(unit)
        player.discarded_units.append(unit)
        board.board[row][col] = unit[0]
        player.control_tokens -= 1
        player.control_zones.append([row, col])
        player.units_on_board.add(unit)

    @staticmethod
    def move(player, board):
        unit = Action.__prompt_user_for_unit_name(
            'Which unit from your hand and on the board would you like to move? ',
            lambda unit: (unit not in player.units_on_board),
            player)

        from_row, from_col = Action.__prompt_user_for_position(
            'From position (row, col): ',
            (lambda from_row, from_col: not board.board[from_row][from_col] == unit[0]),
            board)

        to_row, to_col = Action.__prompt_user_for_position(
            'From position (row, col): ', (), board)
        # ToDo: check move condition for specific unit

        board.board[from_row][from_col] = '.'
        board.board[to_row][to_col] = unit[0]
        player.hand.remove(unit)
        player.discarded_units.append(unit)

    @staticmethod
    def recruit(player):
        unit = Action.__prompt_user_for_unit_name(
            'Which unit would you like to discard from your hand to recruit the same kind? ', (), player)

        if player.recruitment_pieces[unit] <= 0:
            print(f'You don\'t have more units of type {unit} to recruit.')
            return

        player.hand.remove(unit)
        player.discarded_units.append(unit)
        player.bag.append(unit)
        player.recruitment_pieces[unit] -= 1

        print(f'{unit} successfully discarded from hand and added to bag!\n')

    @staticmethod
    def attack(player, opponent, board):
        unit = Action.__prompt_user_for_unit_name(
            'Which unit from your hand and on the board would you like to use for attack? ',
            (lambda unit: unit not in player.units_on_board),
            player)

        unit_to_attack = Action.__prompt_user_for_unit_name(
            'Which opponent\'s unit on the board would you like to attack? ',
            (lambda unit_to_attack: unit_to_attack not in opponent.units_on_board),
            opponent)

        row, col = Action.__prompt_user_for_position(
            f'Which position would you like {unit} to attack (row,col)? ',
            (lambda row, col: [row, col] not in opponent.control_zones),
            board)
        # ToDo: check attack condition for specific unit

        player.hand.remove(unit)
        player.discarded_units.append(unit)
        board.board[row][col] = unit[0]

        Action.__delete_attacked_unit(opponent, unit_to_attack)

    @staticmethod
    def initiative(player):
        unit = Action.__prompt_user_for_unit_name('Which unit would you like to discard from your hand? ', (), player)

        player.hand.remove(unit)
        player.discarded_units.append(unit)
        player.initiative = True

        print(f'{unit} successfully discarded from hand! You have the initiative for next round!\n')

    @staticmethod
    def __delete_attacked_unit(player, unit):
        player.units_on_board.remove(unit)
        player.recruitment_pieces.pop(unit)
        player.bag.remove(unit)
        player.discarded_units.remove(unit)
        player.hand.remove(unit)

    @staticmethod
    def __is_position_valid(row, col, size):
        return 0 <= row < size and 0 <= col < size

    @staticmethod
    def __is_unit_valid(unit, player):
        return unit in Action.UNIT_TYPES and unit in player.hand

    @staticmethod
    def __prompt_user_for_unit_name(message, condition, player):
        unit = input(message)
        while not Action.__is_unit_valid(unit, player) or condition:
            unit = input('Invalid unit. ' + message)

        return unit

    @staticmethod
    def __prompt_user_for_position(message, condition, board):
        row, col = list(map(int, input(message).split(',')))
        while not Action.__is_position_valid(row, col, board.SIZE) or condition:
            row, col = list(map(int, input('Invalid position. ' + message).split(',')))

        return row, col
