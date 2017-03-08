# 1 plat land
# 2 water
# 6 plat land
from enum import Enum


class Map:
    def __init__(self):
        self.tiles = [
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        ]
        pass

    def getSize(self):
        # (width, height) including edges
        return (11, 8)

    def getStartPos(self):
        # (x, y) counting from 0
        return (1, 1)

    def getEndPos(self):
        # (x, y) counting from 0
        return (9, 6)

    def getTiles(self):
        # 0 = land, 1 = water
        return list(map(list, zip(*self.tiles)))  # transposed

    def toggleTile(self, i, j):
        self.tiles[j][i] = 1 - self.tiles[j][i]

    def getScenery(self):
        pass


class Tile(Enum):
    LAND = 0
    WATER = 1
