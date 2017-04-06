from src.alg.ACO import ACO
from src.gui.GUI import GUI
from src.map.Map import Map

map = Map()
alg = ACO(map)  # start with ACO
GUI(map, alg)
