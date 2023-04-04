from data import fullLoad, readGraph
from algorithms.dijkstra import dijkstra
from algorithms.astar import aStar

if __name__=="__main__":
    #fullLoad()
    city = readGraph()
    # dijkstra(city, "Kamienna", "Kopańskiego", "9:55:00")
    aStar(city, "LEŚNICA", "KSIĘŻE MAŁE", "10:00:00", 't')