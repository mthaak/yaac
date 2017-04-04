from src.alg.ASRanked import ASRanked
from src.gui.GUI import GUI
from src.map.Map import Map

map = Map()
alg = ASRanked(map)
GUI(map, alg)
