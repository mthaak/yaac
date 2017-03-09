import random
from enum import Enum


class Map:
    def __init__(self):
        self.startPos = (1, 1)
        self.endPos = [(9, 6)]

        tiles = [  # 0 = land, 1 = water
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.tiles = list(map(list, zip(*tiles)))  # transposed

        self.props = [
            Prop(1, 1, 90, PropModel.HOLE),  # start
            Prop(9, 6, 0, PropModel.PLANT_1),  # end
            Prop(1, 3, 90, PropModel.GREY_ROCK),
            Prop(1, 6, 270, PropModel.GREY_ROCK),
            Prop(7, 5, 0, PropModel.TREE_LONG),
            Prop(8, 2, 0, PropModel.TREE_ORANGE),
            Prop(9, 4, 0, PropModel.TENT),
        ]

    def getSize(self):
        # (width, height) including map edges
        return (11, 8)

    def getStartPos(self):
        return self.startPos  # (x, y) counting from 0

    def getEndPos(self):
        return self.endPos

    def addEndPos(self, i, j):
        self.endPos.append((i, j))

    def removeEndPos(self, i, j):
        self.endPos.remove((i, j))

    def getTiles(self):
        return self.tiles

    def tileBlocked(self, i, j):
        """A tile is blocked when it contains water, a tree or a rock."""
        if self.tiles[i][j] == 1:
            return True
        for prop in self.props:
            if prop.i == i and prop.j == j \
                    and (prop.model in PropModel.tree() + PropModel.rock()):
                return True
        return False

    def tileOccupied(self, i, j):
        """A tile is occupied when it contains water or any prop."""
        if self.tiles[i][j] == 1:
            return True
        for prop in self.props:
            if prop.i == i and prop.j == j:
                return True
        return False

    def getProps(self):
        return self.props

    def toggleTile(self, i, j):
        self.tiles[i][j] = 1 - self.tiles[i][j]

    def getProp(self, i, j):
        for prop in self.props:
            if prop.i == i and prop.j == j:
                return prop
        return None

    def createProp(self, i, j, r, model):
        self.props.append(Prop(i, j, r, model))

    def removeProp(self, i, j):
        prop = self.getProp(i, j)
        if prop:
            self.props.remove(prop)
            if (i, j) in self.endPos:
                self.removeEndPos(i, j)

    def moveProp(self, oldi, oldj, newi, newj):
        prop = self.getProp(oldi, oldj)
        if prop:
            prop.i, prop.j = newi, newj

    def placeProp(self, prop):
        self.props.append(prop)

    def randomFood(self, i, j):
        return Prop(i, j, random.choice([0, 90, 180, 270]), random.choice(PropModel.food()))

    def randomTree(self, i, j):
        return Prop(i, j, random.choice([0, 90, 180, 270]), random.choice(PropModel.tree()))

    def randomRock(self, i, j):
        return Prop(i, j, random.choice([0, 90, 180, 270]), random.choice(PropModel.rock()))

    def randomDecoration(self, i, j):
        return Prop(i, j, random.choice([0, 90, 180, 270]), random.choice(PropModel.decoration()))


class TileType(Enum):
    LAND = 0
    WATER = 1


class Prop:
    def __init__(self, i, j, r, model):
        assert type(i) == int
        assert type(j) == int
        assert type(r) == int and r in [0, 90, 180, 270]
        assert type(model) == PropModel
        self.i, self.j, self.r, self.model = i, j, r, model


class PropModel(Enum):
    NONE = None
    TENT = 'naturepack_extended/Models/naturePack_107.obj'
    TREE_ORANGE = 'naturepack_extended/Models/naturePack_066.obj'
    TREE_LONG = 'naturepack_extended/Models/naturePack_074.obj'
    GREY_ROCK = 'naturepack_extended/Models/naturePack_060.obj'
    PUMPKIN = 'naturepack_extended/Models/naturePack_170.obj'
    # FLAT
    PLANT_1 = 'naturepack_extended/Models/naturePack_flat_001.obj'
    PLANT_2 = 'naturepack_extended/Models/naturePack_flat_002.obj'
    PLANT_3 = 'naturepack_extended/Models/naturePack_flat_003.obj'
    PLANT_4 = 'naturepack_extended/Models/naturePack_flat_004.obj'
    FLOWER_TALL_BLUE = 'naturepack_extended/Models/naturePack_flat_005.obj'
    FLOWER_BLUE = 'naturepack_extended/Models/naturePack_flat_006.obj'
    FLOWER_TALL_YELLOW = 'naturepack_extended/Models/naturePack_flat_008.obj'
    FLOWER_YELLOW = 'naturepack_extended/Models/naturePack_flat_009.obj'
    FLOWER_RED = 'naturepack_extended/Models/naturePack_flat_010.obj'
    FLOWER_TALL_RED = 'naturepack_extended/Models/naturePack_flat_011.obj'
    PLANT_5 = 'naturepack_extended/Models/naturePack_flat_012.obj'
    PLANT_6 = 'naturepack_extended/Models/naturePack_flat_013.obj'
    # NOT FROM NATUREPACK
    HOLE = 'rabbit_hole.obj'

    @staticmethod
    def food():
        return [PropModel.PLANT_1,
                PropModel.PLANT_2,
                PropModel.PLANT_3,
                PropModel.PLANT_4,
                PropModel.FLOWER_TALL_BLUE,
                PropModel.FLOWER_BLUE,
                PropModel.FLOWER_TALL_YELLOW,
                PropModel.FLOWER_YELLOW,
                PropModel.FLOWER_RED,
                PropModel.FLOWER_TALL_RED,
                PropModel.PLANT_5,
                PropModel.PLANT_6]

    @staticmethod
    def tree():
        return [PropModel.TREE_ORANGE,
                PropModel.TREE_LONG]

    @staticmethod
    def rock():
        return [PropModel.GREY_ROCK]

    @staticmethod
    def decoration():
        return [PropModel.PUMPKIN]

# Define the places of objects.
# Define different objects like trees
# Develop drag and drop of the objects.
# Implement different map layouts: paper describes different grid sizes.
