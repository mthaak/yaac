import random
from enum import Enum

import numpy as np

from src.map.Map import PropModel


class ASRanked:
    def __init__(self, map):
        self.map = map

        self.edges = self.generateEdges()
        self.fixHoles()

        self.entities = [
            Entity(map, 0, 'rabbit', RabbitColor.WHITE, 1, 1, 0, self.edges, 0, False),
            Entity(map, 0, 'rabbit', RabbitColor.GREY, 1, 1, 0, self.edges, 0, False),
            Entity(map, 0, 'rabbit', RabbitColor.BLACK, 1, 1, 0, self.edges, 0, False),
            Entity(map, 0, 'rabbit', RabbitColor.BROWN, 1, 1, 0, self.edges, 0, False),
            Entity(map, 0, 'rabbit', RabbitColor.BEIGE, 1, 1, 0, self.edges, 0, False)
        ]

    def update(self):
        changed = False
        sumhome = 0
        numberofrabbits = 0
        for entity in self.entities:
            sumhome += entity.is_waiting
            numberofrabbits += 1
        if sumhome == numberofrabbits:
            self.updatepheromones()
        for entity in self.entities:
            changed |= entity.updatePos(sumhome == numberofrabbits)
            entity.is_home = (entity.i, entity.j) == entity.home_pos

        return changed

    def updatepheromones(self):
        edges = self.edges
        rho = 0.5  # evaporation rate
        e = 0.5  # factor for the elitest path
        Q = 1
        allpaths, pathranks = self.getAllPaths()
        lengthallpaths = len(allpaths)
        bestPath = self.getBestPathTrail()  # best path globally
        lengthbestpath = len(bestPath)

        for edge in edges:
            evaporation = edges[edge][1] * (1 - rho)
            t_e = 0  # edge is on the best path
            t_k = 0  # edge is on a current solution

            for i in range(1, len(allpaths)):

                rank = pathranks[i]
                path = allpaths[i]
                if edge in path:
                    t_mu = (len(allpaths) - rank) * Q / len(path)
                    t_k += t_mu

            if edge in bestPath:
                t_e = len(allpaths) * Q / lengthbestpath
                # t_best = 1
            edges[edge][1] = (evaporation + t_k + (e * t_e))

            if self.edges[edge][1] < 0.1:  # minimum
                self.edges[edge][1] = 0.1
            elif self.edges[edge][1] > 5:  # maximum
                self.edges[edge][1] = 5

    def placeEntity(self, entity):
        self.entities.append(entity)

    def getEntities(self):
        return self.entities

    def getBestPath(self):
        return min([entity.best_path for entity in self.entities])

    def getBestPathTrail(self):
        bestPathLength = 999  # could be set to upper bound
        bestPath = []
        for entity in self.entities:
            if len(entity.best_path_edges) < bestPathLength:
                bestPathLength = len(entity.way)
                bestPath = entity.best_path_edges
        return bestPath

    def getAllPaths(self):
        allpaths = []
        pathlengts = []
        for entity in self.entities:
            allpaths.append(entity.way)
            pathlengts.append(len(entity.way))
        pathlengts = np.array(pathlengts)
        pathlengts = np.argsort(pathlengts)
        return allpaths, pathlengts

    # def evaporate(self):
    #     rho = 0.05  # evaporation rate
    #     for edge in self.edges:
    #         self.edges[edge][1] *= (1 - rho)
    #         if self.edges[edge][1] < 0.1:
    #             self.edges[edge][1] = 0.1
    #         elif self.edges[edge][1] > 5:
    #             self.edges[edge][1] = 5
    #     return

    def fixEdges(self, i, j):
        """After a tile was toggled or a prop was added or removed, we need to fix the edges."""
        width, height = self.map.getSize()
        if self.map.tileBlocked(i, j):  # remove edges
            edges = [
                (i, j, i, j - 1, 0),
                (i, j, i + 1, j, 90),
                (i, j, i, j + 1, 180),
                (i, j, i - 1, j, 270),
                (i, j - 1, i, j, 180),
                (i + 1, j, i, j, 270),
                (i, j + 1, i, j, 0),
                (i - 1, j, i, j, 90),
            ]
            for edge in edges:
                try:
                    self.edges.pop(edge)
                except KeyError:
                    pass
        else:  # create new edges
            if not self.map.tileBlocked(i, j - 1) and j != 1:
                self.edges[(i, j, i, j - 1, 0)] = [1, 0.1]
                self.edges[(i, j - 1, i, j, 180)] = [1, 0.1]
            if not self.map.tileBlocked(i + 1, j) and i != width - 2:
                self.edges[(i, j, i + 1, j, 90)] = [1, 0.1]
                self.edges[(i + 1, j, i, j, 270)] = [1, 0.1]
            if not self.map.tileBlocked(i, j + 1) and j != height - 2:
                self.edges[(i, j, i, j + 1, 180)] = [1, 0.1]
                self.edges[(i, j + 1, i, j, 0)] = [1, 0.1]
            if not self.map.tileBlocked(i - 1, j) and i != 1:
                self.edges[(i, j, i - 1, j, 270)] = [1, 0.1]
                self.edges[(i - 1, j, i, j, 90)] = [1, 0.1]

    def fixEdgesHole(self, i, j, rotation):
        """Fixes edges for a new hole."""
        width, height = self.map.getSize()
        edges = [
            (i, j, i, j - 1, 0),
            (i, j, i + 1, j, 90),
            (i, j, i, j + 1, 180),
            (i, j, i - 1, j, 270),
            (i, j - 1, i, j, 180),
            (i + 1, j, i, j, 270),
            (i, j + 1, i, j, 0),
            (i - 1, j, i, j, 90),
        ]
        for edge in edges:
            try:
                self.edges.pop(edge)
            except KeyError:
                pass

        if not self.map.tileBlocked(i, j - 1) and j != 1 and rotation == 0:
            self.edges[(i, j, i, j - 1, 0)] = [1, 0.1]
            self.edges[(i, j - 1, i, j, 180)] = [1, 0.1]
        elif not self.map.tileBlocked(i + 1, j) and i != width - 2 and rotation == 90:
            self.edges[(i, j, i + 1, j, 90)] = [1, 0.1]
            self.edges[(i + 1, j, i, j, 270)] = [1, 0.1]
        elif not self.map.tileBlocked(i, j + 1) and j != height - 2 and rotation == 180:
            self.edges[(i, j, i, j + 1, 180)] = [1, 0.1]
            self.edges[(i, j + 1, i, j, 0)] = [1, 0.1]
        elif not self.map.tileBlocked(i - 1, j) and i != 1 and rotation == 270:
            self.edges[(i, j, i - 1, j, 270)] = [1, 0.1]
            self.edges[(i - 1, j, i, j, 90)] = [1, 0.1]

    def tileOccupied(self, i, j):
        for entity in self.entities:
            if entity.i == i and entity.j == j:
                return True
        return False

    def generateEdges(self):
        """Generates all the edges based on the map."""
        edges = {}
        width, height = self.map.getSize()
        for i in range(1, (width - 1)):
            for j in range(1, height - 1):
                if self.map.tileBlocked(i, j):
                    continue
                if not self.map.tileBlocked(i, j - 1) and j != 1:
                    edges[(i, j, i, j - 1, 0)] = [1, 0.1]
                if not self.map.tileBlocked(i + 1, j) and i != width - 2:
                    edges[(i, j, i + 1, j, 90)] = [1, 0.1]
                if not self.map.tileBlocked(i, j + 1) and j != height - 2:
                    edges[(i, j, i, j + 1, 180)] = [1, 0.1]
                if not self.map.tileBlocked(i - 1, j) and i != 1:
                    edges[(i, j, i - 1, j, 270)] = [1, 0.1]
        return edges

    def fixHoles(self):
        for prop in self.map.getProps():
            if prop.model == PropModel.HOLE:
                self.fixEdgesHole(prop.i, prop.j, prop.r)


class Entity:
    def __init__(self, map, index, type, color, i, j, orient, edges, found_food, is_lost):
        self.map = map
        self.index = index
        self.type = 'rabbit'  # TODO create other possibilities
        self.color = color
        self.i = i
        self.j = j
        self.orient = orient
        self.edges = edges
        self.alpha = 10  # This can be anything, and might be variable
        self.beta = 10  # This can be anyting, and might be variable
        self.pherodrop = 1  # the amount of pheromones that is dropped when food is found
        self.max_distance = len(edges) / 2  # if > 0 , the rabbit will return to its home after this many steps
        self.max_distance_reached = False
        self.found_food = found_food
        self.step_count = 0
        self.way = []
        self.way_back = []
        self.start_pos = self.map.getStartPos()
        self.home_pos = (i, j)  # current home of rabbit
        self.end_pos = self.map.getEndPos()
        self.prevpos = ()
        self.best_path = (map.getSize()[0] - 2) * (map.getSize()[1] - 2)
        self.best_path_edges = []
        self.is_lost = is_lost  # whether entity lost its path back to its start
        self.visited_edges = [(i, j)]
        self.food_pos = (0, 0)  # current food of rabbit
        self.is_home = True
        self.is_waiting = False

    def getEdges(self, i, j, edges, prevpos):
        returned_edges = {}
        try:
            if prevpos != (i, j, i, j - 1, 0):
                returned_edges[(i, j, i, j - 1, 0)] = edges[(i, j, i, j - 1, 0)]
        except KeyError:
            pass  # print('no edge down')
        try:
            if prevpos != (i, j, i + 1, j, 90):
                returned_edges[(i, j, i + 1, j, 90)] = edges[(i, j, i + 1, j, 90)]
        except KeyError:
            pass  # print('no edge right')
        try:
            if prevpos != (i, j, i, j + 1, 180):
                returned_edges[(i, j, i, j + 1, 180)] = edges[(i, j, i, j + 1, 180)]
        except KeyError:
            pass  # print('no edge up')
        try:
            if prevpos != (i, j, i - 1, j, 270):
                returned_edges[(i, j, i - 1, j, 270)] = edges[(i, j, i - 1, j, 270)]
        except KeyError:
            pass  # print('no edge left')

        if not returned_edges:
            returned_edges[prevpos] = edges[prevpos]

        for edge in returned_edges:
            # if the direction is the same, we give the edge a bonus
            if edge[4] == self.orient:
                returned_edges[edge][0] = returned_edges[edge][0] * 1.5

            for n in self.visited_edges:
                if n == (edge[2], edge[3]):
                    returned_edges[edge][0] = returned_edges[edge][0] / 8
        # returned_edges[(0,1,0,1)] = edges[(0,1,0,1)] #replace with workable values
        return returned_edges

    def weighted_choice(self, choices):
        total = 1  # can be variable
        r = random.uniform(0, total)
        upto = 0
        for c, w in choices:
            if upto + w >= r:
                return c
            upto += w
        assert False, "Shouldn't get here"

    def reversed_path(self, path):  # returns the reversed path
        i = path[0]
        j = path[1]
        new_i = path[2]
        new_j = path[3]
        orientation = path[4]
        if orientation == 0:
            new_orientation = 180
        elif orientation == 90:
            new_orientation = 270
        elif orientation == 180:
            new_orientation = 0
        else:
            new_orientation = 90
        new_path = (new_i, new_j, i, j, new_orientation)
        return new_path

    def evaporate(self, edges):
        rho = 0.1  # evaporation rate
        for edge in edges:
            edges[edge][1] *= (1 - rho)
            if edges[edge][1] < 0.1:
                edges[edge][1] = 0.1
            elif edges[edge][1] > 5:
                edges[edge][1] = 5

    # def straight_path(self, path): #returns the reversed path
    #     a,b,c,d = path[0], path[1], path[2], path[3]
    #     if a == c: # x axis
    #         if b<d: #move down
    #
    #         else: #move up
    #             if a<c: #move right
    #
    #             else: #move left
    #     return new_path

    def updatePos(self, allrabbitshome):
        i, j = self.i, self.j
        usable_edges = self.getEdges(i, j, self.edges, self.prevpos)

        if self.type == 'rabbit':
            if self.is_lost == 1:  # rabbit is lost
                k = {}
                p = {}
                sum_pheromones = 0
                sum_probability = 0
                list_of_candidates = []
                list_of_probabilities = []
                for edge in usable_edges:  # this loop calculates the sum of weighted pheromones of all options
                    k[edge] = usable_edges[edge]
                    weighted_eta = (
                                       1) ** self.alpha  # pheromone level is not taken into account in finding the way back
                    weighted_pheromone = (k[edge][0]) ** self.beta
                    sum_pheromones += (weighted_pheromone * weighted_eta)
                    list_of_candidates.append(edge)
                for edge in list_of_candidates:  # this loop calculates the probability of the entity taking an edge for every edge
                    k[edge] = usable_edges[edge]
                    weighted_eta = (1) ** self.alpha
                    weighted_pheromone = (k[edge][0]) ** self.beta
                    p[edge] = (weighted_pheromone * weighted_eta) / sum_pheromones
                    list_of_probabilities.append(p[edge])

                    sum_probability += p[edge]  # should be 1 in total

                path = self.weighted_choice(p.items())
                for edge in usable_edges:
                    usable_edges[edge][0] = 1  # reset the heuristic data

                reversed_path = self.reversed_path(path)
                self.current_direction = path[4]
                # print("path =%s" % str(path))

                self.prevpos = (path[2], path[3], path[0], path[1], (path[4] + 180) % 360)
                # path = numpy.random.choice(list_of_candidates, 1, list_of_probabilities) Doesn't work because a should be 1-dimensional
                self.i, self.j, self.orient = path[2], path[3], path[4]  # pick new position randomly

                newpos = (path[2], path[3])
                self.visited_edges.append((path[2], path[3]))

                if newpos in self.start_pos:
                    self.is_lost = False
                    self.visited_edges = [self.visited_edges[0]]
                    self.step_count = 0
                else:
                    return True

                return True
            elif self.found_food == 1:  # FOOD IS FOUND, GO BACK TO STARTING POINT WHILE DROPPING PHEROMONES
                if self.is_waiting == 1:  # home point is reached, and bunny waits for the other bunnies
                    if allrabbitshome == 1:  # all bunnies home, so now update the pheromones
                        for path in self.way:
                            try:
                                self.edges[path][1]
                            except KeyError:
                                print("path removed")

                        self.found_food = 0
                        self.is_waiting = 0
                        self.way = []
                    return True
                else:
                    path = self.way_back.pop()
                    reversed_path = self.reversed_path(path)
                    self.i, self.j, self.orient = path[2], path[3], path[4]

                    try:
                        self.edges[reversed_path][1]
                    except KeyError:  # probably an object was placed on reversed path
                        self.is_lost = True  # TODO have the entity actually be lost and having to find a way back to a home
                        self.found_food = False
                        self.visited_edges = [self.visited_edges[0]]
                        self.way_back = []

                    newpos = (path[2], path[3])
                    if newpos == self.home_pos:
                        self.is_waiting = 1
                        # self.found_food = 0
                        self.way_back = []

                    return True
            elif self.max_distance_reached == True:
                try:
                    path = self.way_back.pop()
                except IndexError:
                    if (self.i, self.j) == self.home_pos:  # we do not know why this can be the case
                        self.max_distance_reached = False
                        self.way_back = []
                        self.way = []
                        return True
                    raise
                reversed_path = self.reversed_path(path)
                self.i, self.j, self.orient = path[2], path[3], path[4]

                try:
                    self.edges[reversed_path][1]
                except KeyError:  # probably an object was placed on reversed path
                    self.is_lost = True
                    self.found_food = False
                    self.visited_edges = [self.visited_edges[0]]
                    self.way_back = []
                    self.way = []
                newpos = (path[2], path[3])
                if newpos == self.home_pos:
                    self.max_distance_reached = False
                    self.way_back = []
                    self.way = []
                return True
            elif usable_edges:
                k = {}
                p = {}
                sum_pheromones = 0
                sum_probability = 0
                list_of_candidates = []
                list_of_probabilities = []
                for edge in usable_edges:  # this loop calculates the sum of weighted pheromones of all options
                    k[edge] = usable_edges[edge]
                    weighted_eta = (k[edge][1]) ** self.alpha
                    weighted_pheromone = (k[edge][0]) ** self.beta
                    sum_pheromones += (weighted_pheromone * weighted_eta)
                    list_of_candidates.append(edge)
                for edge in list_of_candidates:  # this loop calculates the probability of the entity taking an edge for every edge
                    k[edge] = usable_edges[edge]
                    weighted_eta = (k[edge][1]) ** self.alpha
                    weighted_pheromone = (k[edge][0]) ** self.beta
                    p[edge] = (weighted_pheromone * weighted_eta) / sum_pheromones
                    list_of_probabilities.append(p[edge])

                    sum_probability += p[edge]  # should be 1 in total

                path = self.weighted_choice(p.items())
                for edge in usable_edges:
                    usable_edges[edge][0] = 1  # reset the heuristic data

                reversed_path = self.reversed_path(path)
                self.current_direction = path[4]
                self.way_back.append(reversed_path)  # path is prepended so it forms the way back (in reversed order)
                self.way.append(path)
                # print("path =%s" % str(path))

                self.prevpos = (path[2], path[3], path[0], path[1], (path[4] + 180) % 360)
                # path = numpy.random.choice(list_of_candidates, 1, list_of_probabilities) Doesn't work because a should be 1-dimensional
                self.i, self.j, self.orient = path[2], path[3], path[4]  # pick new position randomly

                newpos = (path[2], path[3])
                self.visited_edges.append((path[2], path[3]))

                # Check if the rabbit reached its target
                if newpos in self.end_pos:
                    self.found_food = 1
                    self.food_pos = newpos
                    path_length = len(self.way_back)
                    self.visited_edges = [0]
                    if path_length < self.best_path:
                        self.best_path = path_length
                        self.best_path_edges = self.way

                # check if the rabbit walked its maximum distance
                if len(self.way_back) == self.max_distance:
                    self.max_distance_reached = True  # Set the max distance reached to True, so the rabbit will go home
                    self.visited_edges = []  # reset the visited edges, so the rabbit starts from scratch
                else:
                    return True

                return True

        return False  # not changed

    @staticmethod
    def randomRabbit(map, alg, i, j):
        return Entity(map, 0, 'rabbit', random.choice(list(RabbitColor)), i, j, random.choice([0, 90, 180, 270]),
                      alg.edges, 0, True)


class RabbitColor(Enum):
    WHITE = 0
    GREY = 1
    BLACK = 2
    BROWN = 3
    BEIGE = 4
    ORANGE = 5
