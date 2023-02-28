from player import Player


class Board:
    SIZE = 5
    FREE_ZONE_SYMBOL = '@'
    FREE_ZONE_POSITIONS = ((1, 2), (2, 1), (2, 3), (3, 2))

    def __init__(self):
        self._board = [['.' for _ in range(Board.SIZE)] for _ in range(Board.SIZE)]

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value

    def mark_control_zone(self, player: Player):
        for zone in player.control_zones:
            self.board[zone[0]][zone[1]] = player.name[0]

    def mark_free_zones(self):
        for pos in Board.FREE_ZONE_POSITIONS:
            self.board[pos[0]][pos[1]] = Board.FREE_ZONE_SYMBOL

    def __repr__(self):
        delimiter = '   '
        formatted_board = delimiter + delimiter.join(list(map(str, range(Board.SIZE)))) + '\n' + \
                          delimiter + '___' * (Board.SIZE + 1) + '\n'

        for r in range(Board.SIZE):
            formatted_board += f'{r} | ' + delimiter.join(self.board[r]) + '\n'

        return formatted_board
