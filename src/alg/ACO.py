import random
import numpy
from numpy.random import choice


class ACO:
    def __init__(self, map):
        self.map = map

        self.edges = {}
        width, height = self.map.getSize()

        for i in range(1, (width - 1)):
            for j in range(1, height - 1):
                if j != 1:
                    self.edges[(i, j, i, j - 1, 0)] = [1, 0.1]
                if i != width - 2:
                    self.edges[(i, j, i + 1, j, 90)] = [1, 0.1]
                if j != height - 2:
                    self.edges[(i, j, i, j + 1, 180)] = [1, 0.1]
                if i != 1:
                    self.edges[(i, j, i - 1, j, 270)] = [1, 0.1]

        self.best_path = (width - 1) * (height - 1)

        self.entities = [
            Entity(map, 0, 'random-rabbit', 1, 1, self.edges, 0, self.best_path),
            Entity(map, 0, 'random-rabbit', 1, 1, self.edges, 0, self.best_path),
            Entity(map, 0, 'random-rabbit', 1, 1, self.edges, 0, self.best_path),
            Entity(map, 0, 'random-rabbit', 1, 1, self.edges, 0, self.best_path),
            Entity(map, 0, 'random-rabbit', 1, 1, self.edges, 0, self.best_path),

        ]
        self.best_path = (width-1)*(height-1)

    def update(self):

        changed = False
        for entity in self.entities:
            changed |= entity.updatePos()
        return changed

    def getEntities(self):
        return self.entities

    def evaporate(self):
        rho = 0.05 #evaporation rate

        for edge in self.edges:
            self.edges[edge][1] = (1-rho)*self.edges[edge][1]
            if self.edges[edge][1]<0.1:
                self.edges[edge][1] = 0.1
            elif self.edges[edge][1] >5:
                self.edges[edge][1] = 5

        return



    def removeEdgesFromTile(self): #REMOVE THE TIES TO A WATER SQUARE
        removed_edges = []
        width, height = self.map.getSize()
        for i in range(0, (width)):
            for j in range(0, height):
                if self.map.getTiles()[i][j] == 1:
                    try: #4 times edges in
                        del self.edges[(i, j-1, i, j, 180)]
                    except KeyError:
                        print('nice edge down')
                    try:
                        del self.edges[(i+1, j, i , j, 270)]
                    except KeyError:
                        print('no edge right')
                    try:
                        del self.edges[(i, j+1, i , j, 0)]
                    except KeyError:
                        print('no edge up')
                    try:
                        del self.edges[(i-1, j, i, j, 90)]
                    except KeyError:
                        print('no edge left')

                    try: #4 times edges out
                        del self.edges[(i, j, i, j - 1, 0)]
                    except KeyError:
                        print('nice edge down')
                    try:
                        del self.edges[(i, j, i + 1, j, 90)]
                    except KeyError:
                        print('no edge right')
                    try:
                        del self.edges[(i, j, i , j + 1, 180)]
                    except KeyError:
                        print('no edge up')
                    try:
                        del self.edges[(i, j, i - 1, j, 270)]
                    except KeyError:
                        print('no edge left')
        return


class Entity:
    def __init__(self, map, index, type, i, j, edges, found_food, best_path):
        self.map = map
        self.index = index
        self.type = 'random-rabbit'  # TODO create other possibilities
        self.i = i
        self.j = j
        self.orient = 0
        self.edges = edges
        self.alpha = 2 #This can be anything, and might be variable
        self.beta = 10 #This can be anyting, and might be variable
        self.pherodrop = 1 #the amount of pheromones that is dropped when food is found
        self.found_food = found_food
        self.step_count = 0
        self.way = []
        self.way_back = []
        # self.startpos = self.map.getStartPos()
        self.startpos = (i, j)
        self.endpos = self.map.getEndPos()
        self.prevpos = ()
        self.best_path = best_path

    def getEdges(self, i, j, edges, prevpos):
        returned_edges = {}
        try:
            if prevpos != (i, j, i, j - 1, 0):
                returned_edges[(i, j, i, j - 1, 0)] = edges[(i, j, i, j - 1, 0)]
        except KeyError:
            print('nice edge down')
        try:
            if prevpos != (i, j, i + 1, j, 90):
                returned_edges[(i, j, i + 1, j, 90)] = edges[(i, j, i + 1, j, 90)]
        except KeyError:
            print('no edge right')
        try:
            if prevpos != (i, j, i , j + 1, 180):
                returned_edges[(i, j, i , j + 1, 180)] = edges[(i, j, i , j + 1, 180)]
        except KeyError:
            print('no edge up')
        try:
            if prevpos != (i, j, i - 1, j, 270):
                returned_edges[(i, j, i - 1, j, 270)] = edges[(i, j, i - 1, j, 270)]
        except KeyError:
            print('no edge left')

        if not returned_edges:
            returned_edges[prevpos] = edges[prevpos]
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
        usableEedges = self.getEdges(i,j, self.edges, self.prevpos)

        width, height = self.map.getSize()

        if self.type == 'random-rabbit':
            # if random.random() > 1 - self.moveChance:
            #     open_tiles = [(a, b, o) for (a, b, o) in
            #                   [(i + 1, j, 90), (i - 1, j, 270), (i, j + 1, 181), (i, j - 1, 0)] if
            #                   0 < a < width - 1 and 0 < b < height - 1 and tiles[a][b] == 0]
            #     if open_tiles:  # if there are open tiles
            #         self.i, self.j, self.orient = random.choice(open_tiles)  # pick new position randomly
            #         self.moveChance = 0
            #         return True  # changed
            # else:
            #     self.moveChance += 0.001
            if self.found_food ==1: # FOOD IS FOUND, GO BACK TO STARTING POINT WHILE DROPPING PHEROMONES
                path = self.way_back.pop()
                reversed_path = self.reversed_path(path)
                self.i, self.j, self.orient = path[2], path[3], path[4]
                self.edges[reversed_path][1]= self.edges[reversed_path][1] + self.pherodrop
                newpos = (path[2], path[3])
                if newpos == self.startpos:
                    self.found_food = 0
                return True

            elif usableEedges:
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
                self.way_back.append(reversed_path) #path is prepended so it forms the way back (in reversed order)
                self.way.append(path)
                print("path =%s" % str(path))

                self.prevpos = (path[2], path[3], path[0], path[1], (path[4]+180)%360)
                #path = numpy.random.choice(list_of_candidates, 1, list_of_probabilities) Doesn't work because a should be 1-dimensional
                self.i, self.j, self.orient = path[2], path[3], path[4]  # pick new position randomly

                newpos = (path[2], path[3])

                if newpos == self.endpos:
                    self.found_food = 1
                    path_length = len(self.way_back)
                    if path_length < self.best_path:
                        self.best_path = path_length
                else:
                    return True

                return True






        return False  # not changed

