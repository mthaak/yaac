import random
import numpy
from numpy.random import choice


class ACO:
    def __init__(self, map):
        self.map = map

        self.edges = {}
        width, height = self.map.getSize()
        self.edges[(0,1,0,1)] = [2,1]

        for i in range(0, (width)):
            if (i==0):
                for j in range(0, height):
                    if (j == 0):
                        self.edges[(i, j, i + 1, j, 270)] = [1, 1]
                        self.edges[(i, j, i, j + 1, 0)] = [1, 1]
                    elif (j== (height-1)):
                        self.edges[(i, j, i + 1, j, 270)] = [1, 1]
                        self.edges[(i, j, i, j - 1, 180)] = [1, 1]
                    else:
                        self.edges[(i, j, i, j - 1, 180)] = [1, 1]
                        self.edges[(i, j, i + 1, j, 270)] = [1, 1]
                        self.edges[(i, j, i, j + 1, 0)] = [1, 1]
            elif ( i==(width -1)):
                for j in range(0, height ):
                    if (j == 0):
                        self.edges[(i, j, i, j + 1, 0)] = [1, 1]
                        self.edges[(i, j, i - 1, j, 90)] = [1, 1]
                    elif(j==(height-1)):
                        self.edges[(i, j, i, j - 1, 180)] = [1, 1]
                        self.edges[(i, j, i - 1, j, 90)] = [1, 1]
                    else:
                        self.edges[(i, j, i, j - 1, 180)] = [1, 1]
                        self.edges[(i, j, i, j + 1, 0)] = [1, 1]
                        self.edges[(i, j, i - 1, j, 90)] = [1, 1]
            else:
                for j in range(0, height):
                    if (j == 0):
                        self.edges[(i, j, i + 1, j, 270)] = [1, 1]
                        self.edges[(i, j, i, j + 1, 0)] = [1, 1]
                        self.edges[(i, j, i - 1, j, 90)] = [1, 1]
                    elif(j==(height-1)):
                        self.edges[(i, j, i, j - 1, 180)] = [1, 1]
                        self.edges[(i, j, i + 1, j, 270)] = [1, 1]
                        self.edges[(i, j, i - 1, j, 90)] = [1, 1]
                    else: #base case
                        self.edges[(i, j, i, j - 1, 180)] = [1, 1]
                        self.edges[(i, j, i + 1, j, 270)] = [1, 1]
                        self.edges[(i, j, i, j + 1, 0)] = [1, 1]
                        self.edges[(i, j, i - 1, j, 90)] = [1, 1]


        self.entities = [
            Entity(map, 0, 'random-rabbit', 2, 2, self.edges, 0),
            Entity(map, 1, 'random-rabbit', 4, 5, self.edges, 0),
            Entity(map, 2, 'random-rabbit', 9, 2, self.edges, 1)
        ]

    def update(self):

        changed = False
        for entity in self.entities:
            changed |= entity.updatePos()
        return changed

    def getEntities(self):
        return self.entities

    def evaporate(self):
        rho = 0.1 #evaporation rate

        for edge in self.edges:
            self.edges[edge][1] = (1-rho)*self.edges[edge][1]
            if self.edges[edge][1]<1:
                self.edges[edge][1] = 1
        return



class Entity:
    def __init__(self, map, index, type, i, j, edges, found_food):
        self.map = map
        self.index = index
        self.type = 'random-rabbit'  # TODO create other possibilities
        self.i = i
        self.j = j
        self.orient = 0
        self.edges = edges
        self.alpha = 2 #This can be anything, and might be variable
        self.beta = 2 #This can be anyting, and might be variable
        self.found_food = found_food
        self.step_count = 0
        self.way_back = []

    def getEdges(self, i, j, edges):
        returned_edges = {}
        try:
            returned_edges[(i, j, i, j - 1, 180)] = edges[(i, j, i, j - 1, 180)]
        except KeyError:
            print('nice try')
        try:
            returned_edges[(i, j, i + 1, j, 270)] = edges[(i, j, i + 1, j, 270)]
        except KeyError:
            print('nice try')
        try:
            returned_edges[(i, j, i , j + 1, 0)] = edges[(i, j, i , j + 1, 0)]
        except KeyError:
            print('nice try')
        try:
            returned_edges[(i, j, i - 1, j, 90)] = edges[(i, j, i - 1, j, 90)]
        except KeyError:
            print('nice try')

        #returned_edges[(0,1,0,1)] = edges[(0,1,0,1)] #replace with workable values
        return returned_edges

    def weighted_choice(self, choices):
        total = 1 #can be variable
        r = random.uniform(0, total)
        upto = 0
        for c, w in choices:
            if upto + w >= r:
                return c
            upto += w
        assert False, "Shouldn't get here"

    def reversed_path(self, path): #returns the reversed path
        i = path[0]
        j =  path[1]
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

    def updatePos(self):
        i, j = self.i, self.j
        tiles = self.map.getTiles()
        usableEedges = self.getEdges(i,j, self.edges)
        width, height = self.map.getSize()

        if self.type == 'random-rabbit':
            # if random.random() > 1 - self.moveChance:
            #     open_tiles = [(a, b, o) for (a, b, o) in
            #                   [(i + 1, j, 270), (i - 1, j, 90), (i, j + 1, 0), (i, j - 1, 180)] if
            #                   0 < a < width - 1 and 0 < b < height - 1 and tiles[a][b] == 0]
            #     if open_tiles:  # if there are open tiles
            #         self.i, self.j, self.orient = random.choice(open_tiles)  # pick new position randomly
            #         self.moveChance = 0
            #         return True  # changed
            # else:
            #     self.moveChance += 0.001
            if usableEedges:
                k={}
                p={}
                sum_pheromones = 0
                sum_probability= 0
                list_of_candidates = []
                list_of_probabilities = []
                for edge in usableEedges: #this loop calculates the sum of weighted pheromones of all options
                    k[edge] = usableEedges[edge]
                    weighted_eta = (k[edge][1])**self.alpha
                    weighted_pheromone = (k[edge][0])**self.beta
                    sum_pheromones += (weighted_pheromone * weighted_eta)
                    list_of_candidates.append(edge)
                for edge in list_of_candidates: #this loop calculates the probability of the entity taking an edge for every edge
                    k[edge] = usableEedges[edge]
                    weighted_eta = (k[edge][1])**self.alpha
                    weighted_pheromone = (k[edge][0])**self.beta
                    p[edge] = (weighted_pheromone * weighted_eta)/sum_pheromones
                    list_of_probabilities.append(p[edge])

                    sum_probability += p[edge] #should be 1 in total

                path = self.weighted_choice(p.items())
                reversed_path = self.reversed_path(path)
                self.way_back.append(reversed_path) #path is appended so it forms the way back (in reversed order)
                print("path =%s" % str(path))
                #path = numpy.random.choice(list_of_candidates, 1, list_of_probabilities) Doesn't work because a should be 1-dimensional
                self.i, self.j, self.orient = path[2], path[3], path[4]  # pick new position randomly
                if (self.found_food ==1): #food found, pheromone should be dropped
                    self.edges[path][1]= self.edges[path][1] +1
                    self.edges[reversed_path][1] = self.edges[reversed_path][1] +1
                else:
                    return True

                return True






        return False  # not changed

