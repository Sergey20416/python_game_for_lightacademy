class Player:
    def __init__(self, name, tag):
        self.health = 100
        self.name = name
        self.tag = tag

    # Отнимает указанное количество здоровья
    def damage(self, value):
        if (self.health - value) < 0:
            self.health = 0
        else:
            self.health -= value
        return self.health

    # Прибавляет указанное количество здоровья
    def healing(self, value):
        if (self.health + value) > 100:
            self.health = 100
        else:
            self.health += value
        return self.health
