import unittest
from unittest import mock

from game.action import Action
from game.main import Game


class ActionTest(unittest.TestCase):
    player = None
    opponent = None
    board = None

    def setUp(self):
        game = Game()
        turns, board = game.setup()

        ActionTest.board = board
        ActionTest.player, ActionTest.opponent = turns

        game._Game__randomly_generate_hand(ActionTest.player)
        game._Game__randomly_generate_hand(ActionTest.opponent)

    def test_classVariables_shouldBeCorrectAndAccessible(self):
        unit_types = ('Knight', 'Crossbowman', 'Mercenary', 'Archer')

        self.assertEqual(unit_types, Action.UNIT_TYPES)

    @mock.patch('builtins.input')
    def test_actionPlace_whenValidUserInput_shouldPlaceUnitOnBoard(self, mocked_input):
        unit_to_place = ActionTest.player.hand[0]
        position_to_place = '4,0'
        mocked_input.side_effect = [unit_to_place, position_to_place]

        Action.place(ActionTest.player, ActionTest.board)

        self.assertEqual(ActionTest.board.board[4][0], unit_to_place[0])
        self.assertEqual(len(ActionTest.player.hand), 2)
        self.assertEqual(len(ActionTest.player.units_on_board), 1)

    @mock.patch('builtins.input')
    def test_actionPlace_whenNoControlZones_shouldReturnNone(self, mocked_input):
        unit_to_place = ActionTest.player.hand[0]
        position_to_place = '4,0'
        mocked_input.side_effect = [unit_to_place, position_to_place]
        ActionTest.player.control_zones = []

        res = Action.place(ActionTest.player, ActionTest.board)

        self.assertIsNone(res)

    @mock.patch('builtins.input')
    def test_actionInitiative_whenValidInput_shouldDiscardUnitAndChangeInitiative(self, mocked_input):
        unit_to_discard = ActionTest.player.hand[0]
        mocked_input.side_effect = [unit_to_discard]

        Action.initiative(ActionTest.player)

        self.assertEqual(len(ActionTest.player.hand), 2)
        self.assertEqual(len(ActionTest.player.discarded_units), 1)
        self.assertEqual(ActionTest.player.initiative, True)

    @mock.patch('builtins.input')
    def test_actionRecruit_whenValidInputAndRecruitmentPieces_shouldDiscardUnitAndAddToBag(self, mocked_input):
        unit_to_recruit = ActionTest.player.hand[0]
        unit_to_recruit_count = ActionTest.player.recruitment_pieces[unit_to_recruit]
        mocked_input.side_effect = [unit_to_recruit]

        Action.recruit(ActionTest.player)

        self.assertEqual(len(ActionTest.player.hand), 2)
        self.assertEqual(len(ActionTest.player.discarded_units), 1)
        self.assertEqual(len(ActionTest.player.bag), 2)
        self.assertEqual(ActionTest.player.recruitment_pieces[unit_to_recruit], unit_to_recruit_count - 1)

    @mock.patch('builtins.input')
    def test_actionRecruit_whenNoRecruitmentPieces_shouldReturnNone(self, mocked_input):
        unit_to_recruit = ActionTest.player.hand[0]
        mocked_input.side_effect = [unit_to_recruit]
        ActionTest.player.recruitment_pieces[unit_to_recruit] = 0

        res = Action.recruit(ActionTest.player)

        self.assertIsNone(res)

    def test_isPositionValid_whenValid_shouldReturnTrue(self):
        row = 3
        col = 2
        size = 5

        res = Action()._Action__is_position_valid(row, col, size)

        self.assertTrue(res)

    def test_isPositionValid_whenInvalid_shouldReturnFalse(self):
        row = 6
        col = 2
        size = 5

        res = Action()._Action__is_position_valid(row, col, size)

        self.assertFalse(res)

    def test_isUnitValid_whenValid_shouldReturnTrue(self):
        unit = ActionTest.player.hand[0]

        res = Action()._Action__is_unit_valid(unit, ActionTest.player)

        self.assertTrue(res)

    def test_isUnitValid_whenNotInHand_shouldReturnFalse(self):
        unit = ActionTest.opponent.hand[0]

        res = Action()._Action__is_unit_valid(unit, ActionTest.player)

        self.assertFalse(res)

    def test_isUnitValid_whenNotInUnitTypes_shouldReturnFalse(self):
        unit = 'Not an unit type'

        res = Action()._Action__is_unit_valid(unit, ActionTest.player)

        self.assertFalse(res)

    @mock.patch('builtins.input')
    def test_promptUserForUnitName_whenValid_shouldReturnUnitName(self, mocked_input):
        unit = ActionTest.player.hand[0]
        mocked_input.side_effect = [unit]
        message = 'Test message'

        res = Action()._Action__prompt_user_for_unit_name(message, (), ActionTest.player)

        self.assertEqual(res, unit)

    @mock.patch('builtins.input')
    def test_promptUserForUnitName_whenInvalid_shouldReturnUnitName(self, mocked_input):
        invalid_unit = 'Invalid unit name'
        unit = ActionTest.player.hand[0]
        mocked_input.side_effect = [invalid_unit, unit]
        message = 'Test message'

        res = Action()._Action__prompt_user_for_unit_name(message, (), ActionTest.player)

        self.assertEqual(res, unit)
