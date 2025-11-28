class character():
    def __init__(self, name, life):
        self._name = name
        self.__life = life

    def atack(self, damage):
        return damage


class warrior(character):
    def atack(self, damage):
        return damage * 20


class wizard(character):
    def atack(self, damage):
        return damage + 10

    @property
    def name(self):
        return self._name

    @property
    def life(self):
        return self.__life

    @life.setter
    def life(self, value):
        self.__life = value


w = wizard("kersseek", 100)
w.life = 9
print(w.atack(20), w.name, w.life)
