import unittest
from game.player import Player


class PlayerTest(unittest.TestCase):

    def test_playerInit_withGivenName_shouldBeInitialized(self):
        name = 'Test Player name'
        control_zones = []
        bag = []
        hand = []
        recruitment_pieces = {}
        discarded_units = []
        control_tokens = 3
        units_on_board = set()
        initiative = False

        player = Player(name)

        self.assertEqual(name, player.name)
        self.assertEqual(control_zones, player.control_zones)
        self.assertEqual(bag, player.bag)
        self.assertEqual(hand, player.hand)
        self.assertEqual(recruitment_pieces, player.recruitment_pieces)
        self.assertEqual(discarded_units, player.discarded_units)
        self.assertEqual(control_tokens, player.control_tokens)
        self.assertEqual(units_on_board, player.units_on_board)
        self.assertEqual(initiative, player.initiative)

    def test_classVariables_shouldBeCorrectAndAccessible(self):
        bag_size = 4
        unit_count = 2

        self.assertEqual(bag_size, Player.BAG_SIZE)
        self.assertEqual(unit_count, Player.UNIT_COUNT)

    def test_playerRepr_whenInvoked_shouldReturnCorrectStr(self):
        player_repr = f'======== TEST PLAYER NAME ========\n' \
                      f'Hand: test hand\n' \
                      f'Recruitment pieces: test piece = 2, test piece2 = 3\n' \
                      f'Discard pile: \n' \
                      f'Control tokens: 3\n'

        player = Player('Test Player name')
        player.hand.append('test hand')
        player.recruitment_pieces['test piece'] = 2
        player.recruitment_pieces['test piece2'] = 3

        self.assertEqual(player_repr, str(player))
