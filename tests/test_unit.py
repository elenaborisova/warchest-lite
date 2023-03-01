import unittest

from game.unit import Unit
from game.player import Player


class UnitTypeTest(unittest.TestCase):
    def test_unitInit_whenValidValues_shouldBeInitialized(self):
        # Arrange
        name = 'Unit type test name'
        count = 5
        attack_space = 3
        move_space = 2

        # Act
        unit = Unit(name, count, attack_space, move_space)

        # Assert
        self.assertEqual(name, unit.name)
        self.assertEqual(count, unit.count)
        self.assertEqual(attack_space, unit.attack_space)
        self.assertEqual(move_space, unit.move_space)

    def test_unitInit_whenInvalidCount_shouldRaiseException(self):
        name = 'Unit type test name'
        count = -5
        attack_space = 3
        move_space = 2

        with self.assertRaises(ValueError):
            Unit(name, count, attack_space, move_space)

    def test_unitInit_whenInvalidAttackSpace_shouldRaiseException(self):
        name = 'Unit type test name'
        count = 5
        attack_space = -3
        move_space = 2

        with self.assertRaises(ValueError):
            Unit(name, count, attack_space, move_space)

    def test_unitInit_whenInvalidMoveSpace_shouldRaiseException(self):
        name = 'Unit type test name'
        count = 5
        attack_space = 3
        move_space = -2

        with self.assertRaises(ValueError):
            Unit(name, count, attack_space, move_space)

    def test_unitRepr_whenInvoked_shouldReturnUnitName(self):
        name = 'Unit type test name'
        count = 5
        attack_space = 3
        move_space = 2

        unit = Unit(name, count, attack_space, move_space)

        self.assertEqual(name, str(unit))

    def test_unitCanBePlacedAtPos_whenValidPos_shouldBePlaced(self):
        player = Player('Test player')
        player.control_zones.append([2, 2])

        self.assertTrue(Unit.can_move_to_pos(player.control_zones, [1, 2]))
        self.assertTrue(Unit.can_move_to_pos(player.control_zones, [3, 2]))
        self.assertTrue(Unit.can_move_to_pos(player.control_zones, [2, 1]))
        self.assertTrue(Unit.can_move_to_pos(player.control_zones, [2, 3]))

    def test_unitCanBePlacedAtPos_whenInvalidPos_shouldBePlaced(self):
        player = Player('Test player')
        player.control_zones.append([0, 0])

        self.assertFalse(Unit.can_move_to_pos(player.control_zones, [0, 0]))
        self.assertFalse(Unit.can_move_to_pos(player.control_zones, [0, 2]))
        self.assertFalse(Unit.can_move_to_pos(player.control_zones, [0, 10]))
