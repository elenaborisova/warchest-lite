class Unit:
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

    @property
    def attack_space(self):
        return self._attack_space

    @attack_space.setter
    def attack_space(self, value):
        if value < 0:
            raise ValueError('Attack space should be greater or equal to 0.')

    @property
    def move_space(self):
        return self._move_space

    @move_space.setter
    def move_space(self, value):
        if value < 0:
            raise ValueError('Move space should be greater or equal to 0.')

    def __repr__(self):
        return self.name
