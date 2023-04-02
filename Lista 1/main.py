from data import fullLoad, readGraph
from algorithms.dijkstra import dijkstra

if __name__=="__main__":
    city = readGraph()
    #asa(city, "krzyki", "racławicka")
    dijkstra(city, "Krzyki", "Racławicka", "10:00:00")