from src.alg.EAS2 import EAS2
from src.gui.GUI import GUI
from src.map.Map import Map

map = Map()
alg = EAS2(map)
GUI(map, alg)
