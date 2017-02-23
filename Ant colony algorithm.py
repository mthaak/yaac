import math
import  Tkinter
import random
from time import sleep
import PIL


alfa = 1
beta = 1


class Ant:
    def __init__(self):
        self.Action = 'SearchNextNode'
        self.Node
        self.Path = []
        self.Pathlength = 0
        self.ToVisit = []
        self.Visited = []

    def moves(self):
        if self.Action == 'GoToNode':
            self.goToNode()
        if self.Action == 'SearchNextNode':
            self.searchNextNode()
        if self.Action == 'ReturnToStart':
            self.returnToStart()
        if self.Action == 'GoToFirst':
            self.goToFirst()
    def setCurrentPosition(self):
        nodeindex = self.Node.ID



    def searchNextNode(self):
        nodeindex=self.Node.ID
        pMax = 0 #max probability
        p = 0
        for i in range(NbNodes):
            if i!=self.Node.ID and self.Visited[i]==0:
                d = Land.Distances[self.Node.ID[i]]
                pi = Land.Edges[self.Node.ID[i]]
            if d ==0:
                print i
                print self.Node.ID
            nij = 1/d
            pselected = math.pow(pi,alfa) * math.pow(nij,beta)


    def checkEndingPoint(self):
        False
    def checkBestPathSoFar(self):
        False

    def storePath(self):
        False
    def p_evaporation(self):
        False
    def updateP(self):
        False
    def maxIteration(self):
        False


class Node:
    def __init__(self, x_coordinate, y_coordinate, pheromone_a, pheromone_b, obstacle):
        self.x = x_coordinate
        self.y = y_coordinate

class Edge:
    def __init__(self, pheromone, obstacle, length):
        self.phero = pheromone
        self.obstacle = obstacle
        self.quality = 1/length


Set_edges=[]




x = Node(2, 3, 5.2, 5.3, 2)
print(x.x, x.y, x.phero_a, x.phero_b, x.obstacle)

def Start():
    MainWindow = Tkinter.Tk()   # creates the main window
    MainWindow.title('Ants')
    MainWindow.GParent = MainWindow

    Frame = Ant_Frame(MainWindow, 80)

    # displaying the window
    MainWindow.lift()
    MainWindow.focus_force()
    # Entering main loop
    MainWindow.mainloop()   # control is given to the window system
    OptimalPath=10000000000