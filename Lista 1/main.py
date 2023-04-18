from data import fullLoad, readGraph, fetchLines
from structures import Departure
from algorithms.dijkstra import dijkstra
from algorithms.astar import aStar

if __name__=="__main__":
    #fullLoad()
    city = readGraph()
    dijkstra(city, "LEŚNICA", "KSIĘŻE MAŁE", "7:30:00")
    aStar(city, "LEŚNICA", "KSIĘŻE MAŁE", "7:30:00", 'p')
    aStar(city, "LEŚNICA", "KSIĘŻE MAŁE", "7:30:00", 't')