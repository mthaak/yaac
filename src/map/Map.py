import random
from enum import Enum


class Map:
    def __init__(self):
        self.initMap()
        self.setStartingPoints()
        self.setEndPoints()

    def initMap(self):
        self.size = (11, 8)
        self.current_map = 0;
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

    def smallMap(self):
        self.size = (10, 10)
        self.current_map = 1
        tiles = [
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.tiles = list(map(list, zip(*tiles)))  # transposed

        self.props = [
            Prop(1, 1, 90, PropModel.HOLE),  # start
            Prop(8, 8, 0, PropModel.PLANT_1),  # end
            Prop(1, 7, 90, PropModel.GREY_ROCK),
            Prop(7, 1, 270, PropModel.GREY_ROCK),
            Prop(3, 7, 270, PropModel.GREY_ROCK),
            Prop(5, 8, 270, PropModel.GREY_ROCK),
            Prop(8, 2, 0, PropModel.TREE_LONG),
            Prop(6, 2, 0, PropModel.TREE_LONG),
            Prop(4, 5, 0, PropModel.TREE_ORANGE),
            Prop(8, 7, 0, PropModel.TENT),
        ]

    def mediumMap(self):
        # Still TODO!
        self.size = (15, 15)
        self.current_map = 2
        tiles = [
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.tiles = list(map(list, zip(*tiles)))  # transposed

        self.props = [
            Prop(1, 1, 90, PropModel.HOLE),  # start
            Prop(13, 13, 90, PropModel.FLOWER_RED),  # end
            Prop(1, 7, 90, PropModel.GREY_ROCK),
            Prop(1, 11, 180, PropModel.GREY_ROCK),
            Prop(4, 5, 270, PropModel.GREY_ROCK),
            Prop(6, 5, 180, PropModel.GREY_ROCK),
            Prop(7, 5, 90, PropModel.GREY_ROCK),
            # First row of camping
            Prop(3, 3, 0, PropModel.TENT),
            Prop(4, 3, 0, PropModel.TREE_LONG),
            Prop(4, 4, 0, PropModel.TREE_LONG),
            Prop(6, 3, 0, PropModel.TENT),
            Prop(7, 3, 0, PropModel.TREE_LONG),
            Prop(7, 4, 0, PropModel.TREE_LONG),
            Prop(9, 3, 0, PropModel.TENT),
            Prop(10, 3, 0, PropModel.TREE_LONG),
            Prop(10, 4, 0, PropModel.TREE_LONG),
            # Second row of camping
            Prop(3, 7, 0, PropModel.TENT),
            Prop(4, 7, 0, PropModel.TREE_LONG),
            Prop(4, 8, 0, PropModel.TREE_LONG),
            Prop(6, 7, 0, PropModel.TENT),
            Prop(7, 7, 0, PropModel.TREE_LONG),
            Prop(7, 8, 0, PropModel.TREE_LONG),
            Prop(9, 7, 0, PropModel.TENT),
            Prop(10, 7, 0, PropModel.TREE_LONG),
            Prop(10, 8, 0, PropModel.TREE_LONG),
            # Third row of camping
            Prop(3, 11, 0, PropModel.TENT),
            Prop(4, 11, 0, PropModel.TREE_LONG),
            Prop(4, 12, 0, PropModel.TREE_LONG),
            Prop(6, 11, 0, PropModel.TENT),
            Prop(7, 11, 0, PropModel.TREE_LONG),
            Prop(7, 12, 0, PropModel.TREE_LONG),
            Prop(9, 11, 0, PropModel.TENT),
            Prop(10, 11, 0, PropModel.TREE_LONG),
            Prop(10, 12, 0, PropModel.TREE_LONG),
            # Rocks on the right
            Prop(12, 2, 270, PropModel.GREY_ROCK),
            Prop(12, 4, 270, PropModel.GREY_ROCK),
            Prop(12, 6, 270, PropModel.GREY_ROCK),
            Prop(12, 10, 270, PropModel.GREY_ROCK),
            Prop(12, 12, 270, PropModel.GREY_ROCK),
            # Three orange trees on the left
            Prop(1, 3, 0, PropModel.TREE_ORANGE),
            Prop(1, 9, 90, PropModel.TREE_ORANGE),
            Prop(1, 13, 180, PropModel.TREE_ORANGE),
            # Pumpkins random
            Prop(9, 4, 0, PropModel.PUMPKIN),
            Prop(2, 5, 90, PropModel.PUMPKIN),
            Prop(5, 11, 180, PropModel.PUMPKIN),
            Prop(11, 1, 270, PropModel.PUMPKIN),
            # Top orange trees
            Prop(3, 1, 0, PropModel.TREE_ORANGE),
            Prop(8, 1, 90, PropModel.TREE_ORANGE),
            Prop(13, 1, 180, PropModel.TREE_ORANGE),
            # More end points
            Prop(3, 8, 90, PropModel.FLOWER_TALL_YELLOW),
            Prop(13, 2, 180, PropModel.FLOWER_TALL_BLUE),
            Prop(2, 13, 270, PropModel.FLOWER_TALL_RED),
        ]

    def largeMap(self):
        self.size = (20, 20)
        self.current_map = 3
        tiles = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        ]
        self.tiles = list(map(list, zip(*tiles)))  # transposed

        self.props = [
            Prop(1, 1, 90, PropModel.HOLE),  # start
            Prop(4, 17, 90, PropModel.HOLE), # start
            Prop(3, 18, 90, PropModel.PLANT_5), # end
            Prop(14, 13, 270, PropModel.PLANT_6), # end
            Prop(18, 18, 0, PropModel.FLOWER_TALL_BLUE),  # end
            Prop(13, 4, 90, PropModel.GREY_ROCK),
            Prop(14, 4, 90, PropModel.FLOWER_YELLOW),
            Prop(16, 4, 90, PropModel.FLOWER_YELLOW),
            Prop(12, 4, 90, PropModel.FLOWER_YELLOW),
            Prop(14, 3, 90, PropModel.FLOWER_TALL_RED), # end
            Prop(12, 3, 90, PropModel.FLOWER_TALL_RED), # end
            Prop(16, 3, 90, PropModel.FLOWER_TALL_RED), # end
            Prop(12, 5, 90, PropModel.FLOWER_TALL_BLUE), # end
            Prop(14, 5, 90, PropModel.FLOWER_TALL_BLUE), # end
            Prop(16, 5, 90, PropModel.FLOWER_TALL_BLUE), # end
            Prop(15, 4, 270, PropModel.GREY_ROCK),
            Prop(14, 11, 270, PropModel.GREY_ROCK),
            Prop(14, 12, 90, PropModel.GREY_ROCK),
            Prop(14, 13, 270, PropModel.GREY_ROCK),
            Prop(10, 14, 270, PropModel.GREY_ROCK),
            Prop(3, 11, 0, PropModel.GREY_ROCK),
            Prop(15, 12, 270, PropModel.FLOWER_TALL_RED), # end
            Prop(6, 6, 0, PropModel.TREE_LONG),
            Prop(6, 12, 0, PropModel.TREE_LONG),
            Prop(12, 6, 0, PropModel.TREE_LONG),
            Prop(12, 12, 0, PropModel.TREE_LONG),
            Prop(7, 16, 180, PropModel.TREE_ORANGE),
            Prop(11, 16, 0, PropModel.TREE_ORANGE),
            Prop(15, 11, 0, PropModel.TREE_ORANGE),
            Prop(15, 13, 180, PropModel.TREE_ORANGE),
            Prop(11, 4, 0, PropModel.TREE_ORANGE),
            Prop(7, 4, 0, PropModel.TREE_ORANGE),
            Prop(2, 7, 90, PropModel.TREE_ORANGE),
            Prop(1, 18, 90, PropModel.TREE_ORANGE),
            Prop(9, 9, 0, PropModel.TENT),
            Prop(2, 18, 0, PropModel.PUMPKIN),
            Prop(11, 1, 0, PropModel.PUMPKIN),
        ]

    def toggleMap(self):
        if self.current_map == 0:
            self.smallMap()
        elif self.current_map == 1:
            self.mediumMap()
        elif self.current_map == 2:
            self.largeMap()
        else:
            self.initMap()
        self.setStartingPoints()
        self.setEndPoints()

    def setStartingPoints(self):
        self.start_pos = []
        props = self.props
        for prop in props:
            if prop.model == PropModel.HOLE:
                self.addStartPos(prop.i, prop.j)

    def setEndPoints(self):
        self.end_pos = []
        props = self.props
        for prop in props:
            if prop.model in PropModel.food():
                self.addEndPos(prop.i, prop.j)

    def getSize(self):
        # (width, height) including map edges
        return self.size

    def getStartPos(self):
        return self.start_pos

    def addStartPos(self, i, j):
        self.start_pos.append((i, j))

    def removeStartPos(self, i, j):
        self.start_pos.remove((i, j))

    def getEndPos(self):
        return self.end_pos

    def addEndPos(self, i, j):
        self.end_pos.append((i, j))

    def removeEndPos(self, i, j):
        self.end_pos.remove((i, j))

    def getTiles(self):
        return self.tiles

    def tileBlocked(self, i, j):
        """A tile is blocked when it contains water, a tree or a rock."""
        if self.tiles[i][j] == 1:
            return True
        for prop in self.props:
            if prop.i == i and prop.j == j \
                    and (prop.model in PropModel.trees() + PropModel.rocks() + PropModel.decoration()):
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

    def placeProp(self, prop):
        self.props.append(prop)

    def removeProp(self, i, j):
        prop = self.getProp(i, j)
        if prop:
            self.props.remove(prop)
            if (i, j) in self.end_pos:
                self.removeEndPos(i, j)

    def moveProp(self, oldi, oldj, newi, newj):
        prop = self.getProp(oldi, oldj)
        if prop:
            prop.i, prop.j = newi, newj

    def print(self):
        """Can be used for designing maps within the application."""
        tiles = list(map(list, zip(*self.tiles)))  # transposed
        print('tiles = [')
        for row in tiles:
            print('\t' + repr(row))
        print(']')
        print('props = [')
        for prop in self.props:
            print('\t' + repr(prop))
        print(']')


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

    @staticmethod
    def randomHole(i, j):
        return Prop(i, j, random.choice([0, 90, 180, 270]), PropModel.HOLE)

    @staticmethod
    def randomFood(i, j):
        return Prop(i, j, random.choice([0, 90, 180, 270]), random.choice(PropModel.food()))

    @staticmethod
    def randomTree(i, j):
        return Prop(i, j, random.choice([0, 90, 180, 270]), random.choice(PropModel.trees()))

    @staticmethod
    def randomRock(i, j):
        return Prop(i, j, random.choice([0, 90, 180, 270]), random.choice(PropModel.rocks()))

    @staticmethod
    def randomDecoration(i, j):
        return Prop(i, j, random.choice([0, 90, 180, 270]), random.choice(PropModel.decoration()))

    def __repr__(self):
        return "Prop({0}, {1}, {2}, {3})".format(self.i, self.j, self.r, self.model)


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
    def trees():
        return [PropModel.TREE_ORANGE,
                PropModel.TREE_LONG]

    @staticmethod
    def rocks():
        return [PropModel.GREY_ROCK]

    @staticmethod
    def decoration():
        return [PropModel.PUMPKIN,
                PropModel.TENT]
