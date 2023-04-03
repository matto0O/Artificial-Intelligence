from data import fullLoad, readGraph
from algorithms.dijkstra import dijkstra

if __name__=="__main__":
    #fullLoad()
    city = readGraph()
    #asa(city, "krzyki", "racławicka")
    dijkstra(city, "tarnogaj", "wapienna", "10:00:00")