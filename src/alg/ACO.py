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
        for entity in self.entities:
            entity.updatePos()

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

    def updatePos(self):
        i, j = self.i, self.j
        tiles = self.map.getTiles()
        width, height = self.map.getSize()
        if self.type == 'random-rabbit':
            adjacent_tiles = [(i + 1, j, 90), (i - 1, j, 270), (i, j + 1, 180), (i, j - 1, 0)]
            open_tiles = [(a, b, o) for (a, b, o) in adjacent_tiles if
                          0 < a < width - 1 and 0 < b < height - 1 and tiles[a][b] == 0]
            if len(open_tiles) > 1:  # go forward, left or right
                self.i, self.j, self.orient = random.choice(
                    [(a, b, o) for (a, b, o) in open_tiles if abs(o - self.orient) != 180])  # not back
            else:  # go back
                self.i, self.j, self.orient = open_tiles[0]  # only choice is back
