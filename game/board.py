from player import Player


class Board:
    SIZE = 5

    def __init__(self):
        self.board = [['.' for _ in range(Board.SIZE)] for _ in range(Board.SIZE)]

    def mark_control_zone(self, player: Player):
        for zone in player.control_zones:
            self.board[zone[0]][zone[1]] = player.name[0]

    def mark_free_zones(self):
        POSITIONS = ((1, 2), (2, 1), (2, 3), (3, 2))
        SYMBOL = '@'

        for pos in POSITIONS:
            self.board[pos[0]][pos[1]] = SYMBOL

    def __repr__(self):
        formatted_board = ''
        delimiter = '   '

        formatted_board += '    ' + delimiter.join(list(map(str, range(Board.SIZE)))) + '\n'
        formatted_board += '    ' + '___' * (Board.SIZE + 1) + '\n'

        for r in range(Board.SIZE):
            formatted_board += f'{r} | ' + delimiter.join(self.board[r]) + '\n'

        return formatted_board
