import random
from enum import Enum


class Map:
    def __init__(self):
        self.nr_maps = 4
        self.initMap()
        self.setStartingPoints()
        self.setEndPoints()

    def initMap(self):
        self.size = (11, 8)
        self.current_map = 0
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
            Prop(9, 6, 0, PropModel.PLANT_1),
            Prop(1, 3, 90, PropModel.BROWN_ROCK),
            Prop(1, 6, 270, PropModel.BROWN_ROCK_014),
            Prop(7, 5, 0, PropModel.TREE_SHORT_STUMPS_DARK),
            Prop(8, 2, 0, PropModel.PINE_HEX),
            Prop(9, 4, 0, PropModel.TENT_1),
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
            Prop.randomFood(8, 8),
            Prop.randomRock(1, 7),
            Prop.randomRock(7, 1),
            Prop.randomRock(3, 7),
            Prop.randomRock(5, 8),
            Prop.randomTree(8, 2),
            Prop.randomTree(6, 2),
            Prop.randomTree(4, 5),
            Prop.randomTent(8, 7),
        ]

    def mediumMap(self):
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
            Prop.randomFood(13, 13),
            Prop.randomRock(1, 7),
            Prop.randomRock(1, 11),
            Prop.randomRock(4, 5),
            Prop.randomRock(6, 5),
            Prop.randomRock(7, 5),
            # First row of camping
            Prop.randomTent(3, 3),
            Prop.randomTree(4, 3),
            Prop.randomTree(4, 4),
            Prop.randomTent(6, 3),
            Prop.randomTree(7, 3),
            Prop.randomTree(7, 4),
            Prop.randomTent(9, 3),
            Prop.randomTree(10, 3),
            Prop.randomTree(10, 4),
            # Second row of camping
            Prop.randomTent(3, 7),
            Prop.randomTree(4, 7),
            Prop.randomTree(4, 8),
            Prop.randomTent(6, 7),
            Prop.randomTree(7, 7),
            Prop.randomTree(7, 8),
            Prop.randomTent(9, 7),
            Prop.randomTree(10, 7),
            Prop.randomTree(10, 8),
            # Third row of camping
            Prop.randomTent(3, 11),
            Prop.randomTree(4, 11),
            Prop.randomTree(4, 12),
            Prop.randomTent(6, 11),
            Prop.randomTree(7, 11),
            Prop.randomTree(7, 12),
            Prop.randomTent(9, 11),
            Prop.randomTree(10, 11),
            Prop.randomTree(10, 12),
            # Rocks on the right
            Prop.randomRock(12, 2),
            Prop.randomRock(12, 4),
            Prop.randomRock(12, 6),
            Prop.randomRock(12, 10),
            Prop.randomRock(12, 12),
            # Three orange trees on the left
            Prop.randomTree(1, 3),
            Prop.randomTree(1, 9),
            Prop.randomTree(1, 13),
            # Decoration random
            Prop.randomDecoration(9, 4),
            Prop.randomDecoration(2, 5),
            Prop.randomDecoration(5, 11),
            Prop.randomDecoration(11, 1),
            # Top orange trees
            Prop.randomTree(3, 1),
            Prop.randomTree(8, 1),
            Prop.randomTree(13, 1),
            # More end points
            Prop.randomFood(3, 8),
            Prop.randomFood(13, 2),
            Prop.randomFood(2, 13),
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
            Prop(4, 17, 90, PropModel.HOLE),  # start
            Prop.randomFood(3, 18),
            Prop.randomFood(14, 13),
            Prop.randomFood(18, 18),
            Prop.randomRock(13, 4),
            Prop.randomFlower(14, 4),
            Prop.randomFlower(16, 4),
            Prop.randomFlower(12, 4),
            Prop.randomFlower(14, 3),
            Prop.randomFlower(12, 3),
            Prop.randomFlower(16, 3),
            Prop.randomFlower(12, 5),
            Prop.randomFlower(14, 5),
            Prop.randomFlower(16, 5),
            Prop.randomRock(15, 4),
            Prop.randomRock(14, 11),
            Prop.randomRock(14, 12),
            Prop.randomRock(14, 13),
            Prop.randomRock(10, 14),
            Prop.randomRock(3, 11),
            Prop.randomFlower(15, 12),
            Prop.randomTree(6, 6),
            Prop.randomTree(6, 12),
            Prop.randomTree(12, 6),
            Prop.randomTree(12, 12),
            Prop.randomTree(7, 16),
            Prop.randomTree(11, 16),
            Prop.randomTree(15, 11),
            Prop.randomTree(15, 13),
            Prop.randomTree(11, 4),
            Prop.randomTree(7, 4),
            Prop.randomTree(2, 7),
            Prop.randomTree(1, 18),
            Prop.randomTent(9, 9),
            Prop.randomDecoration(2, 18),
            Prop.randomDecoration(11, 1),
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

    def togglePreviousMap(self):
        if self.current_map == 0:
            self.largeMap()
        elif self.current_map == 1:
            self.initMap()
        elif self.current_map == 2:
            self.smallMap()
        else:
            self.mediumMap()
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
        """A tile is blocked when it is on the edge, it contains water or any prop which blocks the tile."""
        if self.tiles[i][j] == 1 or i == 0 or i == self.size[0] - 1 or j == 0 or j == self.size[1] - 1:
            return True
        blocking_props = PropModel.trees() + PropModel.rocks() + PropModel.tents() + PropModel.decoration()
        for prop in self.props:
            if prop.i == i and prop.j == j and prop.model in blocking_props:
                return True
        return False

    def tileOccupied(self, i, j):
        """A tile is occupied when it is on the edge, it contains water or any prop."""
        if self.tiles[i][j] == 1 or i == 0 or i == self.size[0] - 1 or j == 0 or j == self.size[1] - 1:
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
    def randomFlower(i, j):
        return Prop(i, j, random.choice([0, 90, 180, 270]), random.choice(PropModel.flowers()))

    @staticmethod
    def randomTent(i, j):
        return Prop(i, j, random.choice([0, 90, 180, 270]), random.choice(PropModel.tents()))

    @staticmethod
    def randomDecoration(i, j):
        return Prop(i, j, random.choice([0, 90, 180, 270]), random.choice(PropModel.decoration()))

    def __repr__(self):
        return "Prop({0}, {1}, {2}, {3})".format(self.i, self.j, self.r, self.model)


class PropModel(Enum):
    '''
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
    '''
    FLAT_TILE_DIRT = 'naturepack_extended/Models/naturePack_001.obj'
    RIVER_STRAIGHT_DIRT = 'naturepack_extended/Models/naturePack_002.obj'
    DECLINE_TILE_DIRT = 'naturepack_extended/Models/naturePack_003.obj'
    INCLINE_TILE_DIRT = 'naturepack_extended/Models/naturePack_004.obj'
    INCLINE_TILE_STONE = 'naturepack_extended/Models/naturePack_005.obj'
    FLAT_TILE_STONE = 'naturepack_extended/Models/naturePack_006.obj'
    BROWN_ROCK_007 = 'naturepack_extended/Models/naturePack_007.obj'
    BROWN_ROCK_008 = 'naturepack_extended/Models/naturePack_008.obj'
    BROWN_ROCK_009 = 'naturepack_extended/Models/naturePack_009.obj'
    BROWN_ROCK_010 = 'naturepack_extended/Models/naturePack_010.obj'
    BROWN_ROCK_FLAT_011 = 'naturepack_extended/Models/naturePack_011.obj'
    BROWN_ROCK_FLAT_012 = 'naturepack_extended/Models/naturePack_012.obj'
    BROWN_ROCK_FLAT_013 = 'naturepack_extended/Models/naturePack_013.obj'
    BROWN_ROCK_014 = 'naturepack_extended/Models/naturePack_014.obj'
    BROWN_ROCK_015 = 'naturepack_extended/Models/naturePack_015.obj'
    BROWN_ROCK_016 = 'naturepack_extended/Models/naturePack_016.obj'
    BROWN_ROCK_017 = 'naturepack_extended/Models/naturePack_017.obj'
    BROWN_ROCK_018 = 'naturepack_extended/Models/naturePack_018.obj'
    BROWN_ROCK_019 = 'naturepack_extended/Models/naturePack_019.obj'
    BROWN_ROCK_020 = 'naturepack_extended/Models/naturePack_020.obj'
    BROWN_ROCK_021 = 'naturepack_extended/Models/naturePack_021.obj'
    BROWN_ROCK_022 = 'naturepack_extended/Models/naturePack_022.obj'
    GREY_ROCK_023 = 'naturepack_extended/Models/naturePack_023.obj'
    GREY_ROCK_024 = 'naturepack_extended/Models/naturePack_024.obj'
    GREY_ROCK_025 = 'naturepack_extended/Models/naturePack_025.obj'
    GREY_ROCK_026 = 'naturepack_extended/Models/naturePack_026.obj'
    GREY_ROCK_027 = 'naturepack_extended/Models/naturePack_027.obj'
    GREY_ROCK_028 = 'naturepack_extended/Models/naturePack_028.obj'
    GREY_ROCK_029 = 'naturepack_extended/Models/naturePack_029.obj'
    GREY_ROCK_030 = 'naturepack_extended/Models/naturePack_030.obj'
    GREY_ROCK_031 = 'naturepack_extended/Models/naturePack_031.obj'
    GREY_ROCK_032 = 'naturepack_extended/Models/naturePack_032.obj'
    GREY_ROCK_033 = 'naturepack_extended/Models/naturePack_033.obj'
    BROWN_ROCK_034 = 'naturepack_extended/Models/naturePack_034.obj'
    BROWN_ROCK_035 = 'naturepack_extended/Models/naturePack_035.obj'
    BROWN_ROCK_036 = 'naturepack_extended/Models/naturePack_036.obj'
    BROWN_ROCK_037 = 'naturepack_extended/Models/naturePack_037.obj'
    BROWN_ROCK_038 = 'naturepack_extended/Models/naturePack_038.obj'
    GREY_PILLAR = 'naturepack_extended/Models/naturePack_039.obj'
    GREEN_GRASS_SHORT = 'naturepack_extended/Models/naturePack_040.obj'
    GREEN_GRASS_LONG = 'naturepack_extended/Models/naturePack_041.obj'
    BENCH_SHORT = 'naturepack_extended/Models/naturePack_042.obj'
    GREY_FLAT_043 = 'naturepack_extended/Models/naturePack_043.obj'
    GREY_FLAT_044 = 'naturepack_extended/Models/naturePack_044.obj'
    GREY_FLAT_045 = 'naturepack_extended/Models/naturePack_045.obj'
    STRAIGHT_FENCE = 'naturepack_extended/Models/naturePack_046.obj'
    DIAGONAL_FENCE = 'naturepack_extended/Models/naturePack_047.obj'
    CORNER_FENCE = 'naturepack_extended/Models/naturePack_048.obj'
    BENCH_TALL = 'naturepack_extended/Models/naturePack_049.obj'
    FENCE_HOLE = 'naturepack_extended/Models/naturePack_050.obj'
    PINE_HEX = 'naturepack_extended/Models/naturePack_051.obj'
    PINE_HEX_STUMPS = 'naturepack_extended/Models/naturePack_052.obj'
    PINE_NO_TRUNK = 'naturepack_extended/Models/naturePack_053.obj'
    CACTUS_1_BRANCH = 'naturepack_extended/Models/naturePack_054.obj'
    CACTUS_3_BRANCHES = 'naturepack_extended/Models/naturePack_055.obj'
    CACTUS_3_BRANCHES_SHORT = 'naturepack_extended/Models/naturePack_056.obj'
    STONE_RIVER_TILE_TJUNCTION = 'naturepack_extended/Models/naturePack_057.obj'
    STONE_RIVER_TILE_JUNCTION = 'naturepack_extended/Models/naturePack_058.obj'
    BROWN_ROCK = 'naturepack_extended/Models/naturePack_059.obj'
    GREY_ROCK = 'naturepack_extended/Models/naturePack_060.obj'
    PALM_1 = 'naturepack_extended/Models/naturePack_061.obj'
    TREE_TWO_BRANCHES_DARK = 'naturepack_extended/Models/naturePack_062.obj'
    TREE_THREE_BUSHES_DARK = 'naturepack_extended/Models/naturePack_063.obj'
    TREE_TALL_DARK = 'naturepack_extended/Models/naturePack_064.obj'
    TREE_SHORT_STUMPS_DARK = 'naturepack_extended/Models/naturePack_065.obj'
    TREE_TWO_BRANCHES_FALL = 'naturepack_extended/Models/naturePack_066.obj'
    TREE_THREE_BUSHES_FALL = 'naturepack_extended/Models/naturePack_067.obj'
    TREE_TALL_FALL = 'naturepack_extended/Models/naturePack_068.obj'
    TREE_SHORT_STUMPS_FALL = 'naturepack_extended/Models/naturePack_069.obj'
    TREE_SHORT_STUMPS = 'naturepack_extended/Models/naturePack_070.obj'
    TREE_SHORT_BIG_BUSH = 'naturepack_extended/Models/naturePack_071.obj'
    TREE_TWO_BRANCHES = 'naturepack_extended/Models/naturePack_072.obj'
    TREE_TREE_BUSHES = 'naturepack_extended/Models/naturePack_073.obj'
    TREE_LONG_BUSH = 'naturepack_extended/Models/naturePack_074.obj'
    TENT_1 = 'naturepack_extended/Models/naturePack_075.obj'
    TENT_2 = 'naturepack_extended/Models/naturePack_076.obj'
    STONE_CIRCLE = 'naturepack_extended/Models/naturePack_077.obj'
    CAMPFIRE = 'naturepack_extended/Models/naturePack_078.obj'
    TREE_STUMP = 'naturepack_extended/Models/naturePack_079.obj'
    TREE_STUMP_HUMP = 'naturepack_extended/Models/naturePack_080.obj'
    GREEN_PINE_SHORT = 'naturepack_extended/Models/naturePack_081.obj'
    TRUNK = 'naturepack_extended/Models/naturePack_082.obj'
    GREEN_STONE = 'naturepack_extended/Models/naturePack_083.obj'
    GREEN_PINE = 'naturepack_extended/Models/naturePack_084.obj'
    LAYERED_TREE = 'naturepack_extended/Models/naturePack_085.obj'
    TRUNK_STUMP = 'naturepack_extended/Models/naturePack_086.obj'
    TRUNKLESS_GREEN_PINE_1 = 'naturepack_extended/Models/naturePack_087.obj'
    TRUNKLESS_GREEN_PINE_2 = 'naturepack_extended/Models/naturePack_088.obj'
    TRUNKLESS_GREEN_PINE_3 = 'naturepack_extended/Models/naturePack_089.obj'
    STONE_TILE = 'naturepack_extended/Models/naturePack_090.obj'
    RIVER_CORNER_DIRT = 'naturepack_extended/Models/naturePack_091.obj'
    RIVER_CORNER_STONE = 'naturepack_extended/Models/naturePack_092.obj'
    RIVER_STRAIGHT_STONE = 'naturepack_extended/Models/naturePack_093.obj'
    TREE_LONG_BUSH_FALL = 'naturepack_extended/Models/naturePack_094.obj'
    TENT_3 = 'naturepack_extended/Models/naturePack_095.obj'
    CLIFFS = 'naturepack_extended/Models/naturePack_096.obj'
    GREY_CLIFF_GREEN_TOP = 'naturepack_extended/Models/naturePack_097.obj'
    GREY_CLIFF_CORNER_GREEN_TOP = 'naturepack_extended/Models/naturePack_098.obj'
    GREY_CLIFF_BOTTOM_GREEN_TOP = 'naturepack_extended/Models/naturePack_099.obj'
    GREY_CLIFF_BOTTOM_CORNER_GREEN_TOP = 'naturepack_extended/Models/naturePack_100.obj'
    GREY_CLIFF_END_GREEN_TOP = 'naturepack_extended/Models/naturePack_101.obj'
    GREY_CLIFF_END = 'naturepack_extended/Models/naturePack_102.obj'
    GREY_CLIFF_BOTTOM_CORNER = 'naturepack_extended/Models/naturePack_103.obj'
    GREY_CLIFF_BOTTOM = 'naturepack_extended/Models/naturePack_104.obj'
    GREY_CLIFF_CORNER = 'naturepack_extended/Models/naturePack_105.obj'
    GREY_CLIFF = 'naturepack_extended/Models/naturePack_106.obj'
    TENT_4 = 'naturepack_extended/Models/naturePack_107.obj'
    TRUNK_WITH_HOLE = 'naturepack_extended/Models/naturePack_108.obj'
    TRUNK_WITH_HOLE_STUMP = 'naturepack_extended/Models/naturePack_109.obj'
    WATER_LILY = 'naturepack_extended/Models/naturePack_110.obj'
    MUSHROOM_RED = 'naturepack_extended/Models/naturePack_111.obj'
    MUSHRED_BROWN = 'naturepack_extended/Models/naturePack_112.obj'
    MUSHROOM_TALL = 'naturepack_extended/Models/naturePack_113.obj'
    PINE_SHORT_SQUARE = 'naturepack_extended/Models/naturePack_114.obj'
    TILE_CORNER_DIRT = 'naturepack_extended/Models/naturePack_115.obj'
    CLIFFSBROWN_CLIFF_GREEN_TOP = 'naturepack_extended/Models/naturePack_116.obj'
    BROWN_CLIFF_CORNER_GREEN_TOP = 'naturepack_extended/Models/naturePack_117.obj'
    BROWN_CLIFF_BOTTOM_CORNER_GREEN_TOP = 'naturepack_extended/Models/naturePack_118.obj'
    BROWN_CLIFF_BOTTOM_GREEN_TOP = 'naturepack_extended/Models/naturePack_119.obj'
    BROWN_CLIFF_END_GREEN_TOP = 'naturepack_extended/Models/naturePack_120.obj'
    BROWN_CLIFF = 'naturepack_extended/Models/naturePack_121.obj'
    BROWN_CLIFF_BOTTOM = 'naturepack_extended/Models/naturePack_122.obj'
    BROWN_CLIFF_BOTTOM_CORNER = 'naturepack_extended/Models/naturePack_123.obj'
    BROWN_CLIFF_END = 'naturepack_extended/Models/naturePack_124.obj'
    WATERFALL_TOP_DIRT = 'naturepack_extended/Models/naturePack_125.obj'
    WATERFALL_DIRT = 'naturepack_extended/Models/naturePack_126.obj'
    CLIFF_TOP_DIRT = 'naturepack_extended/Models/naturePack_127.obj'
    CLIFF_CORNER = 'naturepack_extended/Models/naturePack_128.obj'
    OAK_GREEN = 'naturepack_extended/Models/naturePack_129.obj'
    LARGE_OAK_GREEN = 'naturepack_extended/Models/naturePack_130.obj'
    ROCK_6 = 'naturepack_extended/Models/naturePack_131.obj'
    TALL_ROCK_3 = 'naturepack_extended/Models/naturePack_132.obj'
    TALL_ROCK_1 = 'naturepack_extended/Models/naturePack_133.obj'
    ROCK_4 = 'naturepack_extended/Models/naturePack_134.obj'
    ROCK_1 = 'naturepack_extended/Models/naturePack_135.obj'
    ROCK_5 = 'naturepack_extended/Models/naturePack_136.obj'
    ROCK_3 = 'naturepack_extended/Models/naturePack_137.obj'
    FALLEN_TRUNK = 'naturepack_extended/Models/naturePack_138.obj'
    LARGE_OAK_FALL = 'naturepack_extended/Models/naturePack_139.obj'
    OAK_DARK = 'naturepack_extended/Models/naturePack_140.obj'
    GREY_WATERFALL_TOP = 'naturepack_extended/Models/naturePack_141.obj'
    GREY_CLIFF_TOP_CORNER = 'naturepack_extended/Models/naturePack_142.obj'
    GREY_WATERFALL = 'naturepack_extended/Models/naturePack_143.obj'
    RIVER_END_STONE = 'naturepack_extended/Models/naturePack_144.obj'
    RIVER_END_DIRT = 'naturepack_extended/Models/naturePack_145.obj'
    RIVER_TJUNCTION_DIRT = 'naturepack_extended/Models/naturePack_146.obj'
    RIVER_JUNCTION_DIRT = 'naturepack_extended/Models/naturePack_147.obj'
    LONG_TREE_DARK = 'naturepack_extended/Models/naturePack_148.obj'
    LONG_TREE_FALL = 'naturepack_extended/Models/naturePack_149.obj'
    LONG_TREE = 'naturepack_extended/Models/naturePack_150.obj'
    BLOCKY_TREE_DARK = 'naturepack_extended/Models/naturePack_151.obj'
    ROCK_152 = 'naturepack_extended/Models/naturePack_152.obj'
    ROCK_153 = 'naturepack_extended/Models/naturePack_153.obj'
    ROCK_154 = 'naturepack_extended/Models/naturePack_154.obj'
    ROCK_155 = 'naturepack_extended/Models/naturePack_155.obj'
    EASTER_HEAD = 'naturepack_extended/Models/naturePack_156.obj'
    PILLAR = 'naturepack_extended/Models/naturePack_157.obj'
    CUBE = 'naturepack_extended/Models/naturePack_158.obj'
    TALL_PINE = 'naturepack_extended/Models/naturePack_159.obj'
    TALL_PINE_STUMPS = 'naturepack_extended/Models/naturePack_160.obj'
    BLOCK_TREE = 'naturepack_extended/Models/naturePack_161.obj'
    BLOCKY_TREE_FALL = 'naturepack_extended/Models/naturePack_162.obj'
    MEDIUMTALL_PINE = 'naturepack_extended/Models/naturePack_163.obj'
    MEDIUMTALL_PINE_STUMPS = 'naturepack_extended/Models/naturePack_164.obj'
    TALL_PINE_DARK_STUMPS = 'naturepack_extended/Models/naturePack_165.obj'
    TALL_PINE_DARK = 'naturepack_extended/Models/naturePack_166.obj'
    PALM_2 = 'naturepack_extended/Models/naturePack_167.obj'
    PALM_3 = 'naturepack_extended/Models/naturePack_168.obj'
    PALM_4 = 'naturepack_extended/Models/naturePack_169.obj'
    PUMPKIN = 'naturepack_extended/Models/naturePack_170.obj'
    GREY_PUMPKIN = 'naturepack_extended/Models/naturePack_171.obj'
    GREY_FLAT_STONE_172 = 'naturepack_extended/Models/naturePack_172.obj'
    GREY_FLAT_STONE_173 = 'naturepack_extended/Models/naturePack_173.obj'
    GREY_FLAT_STONE_174 = 'naturepack_extended/Models/naturePack_174.obj'
    BROWN_STONE_175 = 'naturepack_extended/Models/naturePack_175.obj'
    PLANT_1 = 'naturepack_extended/Models/naturePack_flat_001.obj'
    PLANT_2 = 'naturepack_extended/Models/naturePack_flat_002.obj'
    PLANT_3 = 'naturepack_extended/Models/naturePack_flat_003.obj'
    PLANT_4 = 'naturepack_extended/Models/naturePack_flat_004.obj'
    FLOWER_TALL_BLUE = 'naturepack_extended/Models/naturePack_flat_005.obj'
    FLOWER_BLUE = 'naturepack_extended/Models/naturePack_flat_006.obj'
    HANGING_MOSS = 'naturepack_extended/Models/naturePack_flat_007.obj'
    FLOWER_TALL_YELLOW = 'naturepack_extended/Models/naturePack_flat_008.obj'
    FLOWER_YELLOW = 'naturepack_extended/Models/naturePack_flat_009.obj'
    FLOWER_RED = 'naturepack_extended/Models/naturePack_flat_010.obj'
    FLOWER_TALL_RED = 'naturepack_extended/Models/naturePack_flat_011.obj'
    FLAT_PLANT = 'naturepack_extended/Models/naturePack_flat_012.obj'
    ROUND_PLANT = 'naturepack_extended/Models/naturePack_flat_013.obj'

    # NOT FROM NATUREPACK
    HOLE = 'rabbit_hole.obj'

    @staticmethod
    def food():
        return [PropModel.PLANT_1,
                PropModel.PLANT_2,
                PropModel.PLANT_3,
                PropModel.PLANT_4,
                PropModel.FLAT_PLANT,
                PropModel.ROUND_PLANT]

    @staticmethod
    def trees():
        return [PropModel.PINE_HEX, PropModel.PINE_HEX_STUMPS, PropModel.PINE_NO_TRUNK,
                PropModel.TREE_TWO_BRANCHES_DARK, PropModel.TREE_THREE_BUSHES_DARK, PropModel.TREE_TALL_DARK,
                PropModel.TREE_SHORT_STUMPS_DARK, PropModel.TREE_TWO_BRANCHES_FALL, PropModel.TREE_THREE_BUSHES_FALL,
                PropModel.TREE_TALL_FALL, PropModel.TREE_SHORT_STUMPS_FALL, PropModel.TREE_SHORT_STUMPS,
                PropModel.TREE_SHORT_BIG_BUSH, PropModel.TREE_TWO_BRANCHES, PropModel.TREE_TREE_BUSHES,
                PropModel.TREE_LONG_BUSH, PropModel.GREEN_PINE_SHORT, PropModel.TRUNKLESS_GREEN_PINE_1,
                PropModel.TRUNKLESS_GREEN_PINE_2, PropModel.TRUNKLESS_GREEN_PINE_3, PropModel.OAK_GREEN,
                PropModel.LARGE_OAK_GREEN, PropModel.LARGE_OAK_FALL, PropModel.OAK_DARK, PropModel.LONG_TREE_DARK,
                PropModel.LONG_TREE_FALL, PropModel.LONG_TREE, PropModel.BLOCKY_TREE_DARK, PropModel.TALL_PINE,
                PropModel.TALL_PINE_STUMPS, PropModel.BLOCK_TREE, PropModel.BLOCKY_TREE_FALL, PropModel.MEDIUMTALL_PINE,
                PropModel.MEDIUMTALL_PINE_STUMPS, PropModel.TALL_PINE_DARK_STUMPS, PropModel.TALL_PINE_DARK]

    @staticmethod
    def rocks():
        return [PropModel.BROWN_ROCK_007, PropModel.BROWN_ROCK_008, PropModel.BROWN_ROCK_009, PropModel.BROWN_ROCK_010,
                PropModel.BROWN_ROCK_014, PropModel.BROWN_ROCK_015, PropModel.BROWN_ROCK_016, PropModel.BROWN_ROCK_017,
                PropModel.BROWN_ROCK_018, PropModel.BROWN_ROCK_019, PropModel.BROWN_ROCK_020, PropModel.BROWN_ROCK_021,
                PropModel.BROWN_ROCK_022, PropModel.BROWN_ROCK_034, PropModel.BROWN_ROCK_035, PropModel.BROWN_ROCK_036,
                PropModel.BROWN_ROCK_037, PropModel.BROWN_ROCK_038, PropModel.BROWN_ROCK, PropModel.ROCK_6,
                PropModel.TALL_ROCK_3, PropModel.TALL_ROCK_1, PropModel.ROCK_4, PropModel.ROCK_1, PropModel.ROCK_5,
                PropModel.ROCK_3, PropModel.ROCK_152, PropModel.ROCK_153, PropModel.ROCK_154, PropModel.ROCK_155]

    @staticmethod
    def flowers():
        return [PropModel.FLOWER_TALL_BLUE, PropModel.FLOWER_BLUE, PropModel.FLOWER_TALL_YELLOW,
                PropModel.FLOWER_YELLOW, PropModel.
                    FLOWER_RED, PropModel.FLOWER_TALL_RED]

    @staticmethod
    def tents():
        return [PropModel.TENT_1, PropModel.TENT_2, PropModel.TENT_3, PropModel.TENT_4]

    @staticmethod
    def decoration():
        return [PropModel.PUMPKIN, PropModel.GREY_PILLAR, PropModel.TREE_STUMP, PropModel.TREE_STUMP_HUMP,
                PropModel.TRUNK, PropModel.TRUNK_STUMP, PropModel.MUSHROOM_RED, PropModel.MUSHRED_BROWN,
                PropModel.MUSHROOM_TALL, PropModel.EASTER_HEAD, PropModel.PILLAR, PropModel.CUBE]
