class Unit:
    def __init__(self, name, count, attack_space, move_space):
        self._name = name
        self._count = count
        self._attack_space = attack_space
        self._move_space = move_space

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
        self._count = value

    @property
    def attack_space(self):
        return self._attack_space

    @attack_space.setter
    def attack_space(self, value):
        self._attack_space = value

    @property
    def move_space(self):
        return self._move_space

    @move_space.setter
    def move_space(self, value):
        self._move_space = value

    def __repr__(self):
        return self.name
