class Player:

    def __init__(self, name):
        self._name = name
        self._control_zones = []
        self._bag = []
        self._hand = []
        self._recruitment_pieces = {}
        self._discarded_units = []
        self._control_tokens = 3
        self._units_on_board = set()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def control_zones(self):
        return self._control_zones

    @control_zones.setter
    def control_zones(self, value):
        self._control_zones = value

    @property
    def bag(self):
        return self._bag

    @bag.setter
    def bag(self, value):
        self._bag = value

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, value):
        self._hand = value

    @property
    def recruitment_pieces(self):
        return self._recruitment_pieces

    @recruitment_pieces.setter
    def recruitment_pieces(self, value):
        self._recruitment_pieces = value

    @property
    def discarded_units(self):
        return self._discarded_units

    @discarded_units.setter
    def discarded_units(self, value):
        self._discarded_units = value

    @property
    def control_tokens(self):
        return self._control_tokens

    @control_tokens.setter
    def control_tokens(self, value):
        self._control_tokens = value

    @property
    def units_on_board(self):
        return self._units_on_board

    @units_on_board.setter
    def units_on_board(self, value):
        self._units_on_board = value

    def __repr__(self):
        return f'======== {self.name.upper()} ========\n' \
               f'Bag: {", ".join(self.bag)}\n' \
               f'Hand: {", ".join(self.hand)}\n' \
               f'Recruitment pieces: {", ".join([f"{k} = {v}" for k, v in self.recruitment_pieces.items()])}\n' \
               f'Discard pile: {", ".join(self.discarded_units)}\n' \
               f'Control tokens: {self.control_tokens}\n'
