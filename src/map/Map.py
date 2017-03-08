# 1 plat land
# 2 water
# 6 plat land
from enum import Enum


class Map:
    def __init__(self):
        self.tiles = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
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
        # width, height = self.getSize()
        # tile = self.tiles[j][i]
        # if tile == Tile.LAND.value:
        #     # Water can always be placed on the sides
        #     if i == 0 or i == width - 1 or j == 0 or j == height - 1:
        #         self.tiles[j][i] = Tile.WATER.value
        #     # Water can be placed adjacent to an existing water tile
        #     else:
        #         water_neighbours = self.tiles[j + 1][i] + self.tiles[j - 1][i] + self.tiles[j][i] + self.tiles[j][i]
        #         if water_neighbours > 0:
        #             self.tiles[j][i] = Tile.WATER.value
        # elif tile == Tile.WATER.value:
        #     self.tiles[j][i] = Tile.LAND.value

    def getScenery(self):
        pass


class Tile(Enum):
    LAND = 0
    WATER = 1
