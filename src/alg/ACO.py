import random


class ACO:
    def __init__(self, map):
        self.map = map
        self.entities = [
            Entity(map, 0, 'random-rabbit', 2, 2),
            Entity(map, 1, 'random-rabbit', 4, 5),
            Entity(map, 2, 'random-rabbit', 9, 2)
        ]

    def update(self):
        changed = False
        for entity in self.entities:
            changed |= entity.updatePos()
        return changed

    def getEntities(self):
        return self.entities


class Entity:
    def __init__(self, map, index, type, i, j):
        self.map = map
        self.index = index
        self.type = 'random-rabbit'  # TODO create other possibilities
        self.i = i
        self.j = j
        self.orient = 0
        self.moveChance = 0

    def updatePos(self):
        i, j = self.i, self.j
        tiles = self.map.getTiles()
        width, height = self.map.getSize()
        if self.type == 'random-rabbit':
            if random.random() > 1 - self.moveChance:
                open_tiles = [(a, b, o) for (a, b, o) in
                              [(i + 1, j, 270), (i - 1, j, 90), (i, j + 1, 0), (i, j - 1, 180)] if
                              0 < a < width - 1 and 0 < b < height - 1 and tiles[a][b] == 0]
                if open_tiles:  # if there are open tiles
                    self.i, self.j, self.orient = random.choice(open_tiles)  # pick new position randomly
                    self.moveChance = 0
                    return True  # changed
            else:
                self.moveChance += 0.001
        return False  # not changed
