from src.alg.ACO import ACO
from src.gui.GUI import GUI
from src.map.Map import Map

map = Map()
alg = ACO(map)
GUI(map, alg)
