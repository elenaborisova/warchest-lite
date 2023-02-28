import unittest
from game.board import Board
from game.player import Player


class BoardTest(unittest.TestCase):

    def test_boardInit_shouldBeInitialized(self):
        board_repr = [['.' for _ in range(5)] for _ in range(5)]

        board = Board()

        self.assertEqual(board_repr, board.board)

    def test_classVariables_shouldBeCorrectAndAccessible(self):
        size = 5
        free_zone_symbol = '@'
        free_zone_positions = ((1, 2), (2, 1), (2, 3), (3, 2))

        self.assertEqual(size, Board.SIZE)
        self.assertEqual(free_zone_symbol, Board.FREE_ZONE_SYMBOL)
        self.assertEqual(free_zone_positions, Board.FREE_ZONE_POSITIONS)

    def test_markControlZones_shouldModifyBoardCorrectly(self):
        player = Player('Test Player name')
        player.control_zones.append([0, 2])
        board = Board()

        board.mark_control_zone(player)

        self.assertEqual('T', board.board[0][2])

    def test_markFreeZones_shouldModifyBoardCorrectly(self):
        board = Board()

        board.mark_free_zones()

        self.assertEqual('@', board.board[1][2])
        self.assertEqual('@', board.board[2][1])
        self.assertEqual('@', board.board[2][3])
        self.assertEqual('@', board.board[3][2])
