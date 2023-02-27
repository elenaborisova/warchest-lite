from player import Player


class Action:
    UNIT_TYPES = ("Archer", "Berserker", "Cavalry", "Crossbowman")

    @staticmethod
    def place(player: Player):
        print('place')

    @staticmethod
    def control(player: Player):
        print('control')

    @staticmethod
    def move(player: Player):
        print('move')

    @staticmethod
    def recruit(player: Player):
        print('recruit')

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
        print('attack')

    @staticmethod
    def initiative(player: Player):
        print('initiative')

        unit = input('Which unit would you like to discard from your hand? ')
        while unit not in Action.UNIT_TYPES or unit not in player.hand:
            unit = input('Invalid unit. Which unit would you like to discard from your hand? ')

        player.hand.remove(unit)
        player.discarded_units.append(unit)

        print(f'{unit} discarded from hand.\n')

