class Unit:
    ADJACENT_POS = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1),
    }

    def __init__(self, name, count, attack_space, move_space):
        self.name = name
        self.count = count
        self.attack_space = attack_space
        self.move_space = move_space

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        if value < 0:
            raise ValueError('Count should be greater or equal to 0.')
        self._count = value

    @property
    def attack_space(self):
        return self._attack_space

    @attack_space.setter
    def attack_space(self, value):
        if value < 0:
            raise ValueError('Attack space should be greater or equal to 0.')
        self._attack_space = value

    @property
    def move_space(self):
        return self._move_space

    @move_space.setter
    def move_space(self, value):
        if value < 0:
            raise ValueError('Move space should be greater or equal to 0.')
        self._move_space = value

    @staticmethod
    def can_move_to_pos(from_pos, to_pos):
        for pos in from_pos:
            for dir in Unit.ADJACENT_POS:
                incr_row = Unit.ADJACENT_POS[dir][0]
                incr_col = Unit.ADJACENT_POS[dir][1]

                if (to_pos[0] == pos[0] + incr_row) and (to_pos[1] == pos[1] + incr_col):
                    return True

        return False

    def __repr__(self):
        return self.name
