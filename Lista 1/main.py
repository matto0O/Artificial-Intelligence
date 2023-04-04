from data import fullLoad, readGraph
from algorithms.dijkstra import dijkstra
from algorithms.astar import asaTimeCriteria, asaTransferCriteria

if __name__=="__main__":
    #fullLoad()
    city = readGraph()
    #dijkstra(city, "leśnica", "księże małe", "10:00:00")
    asaTimeCriteria(city, "leśnica", "księże małe", "10:00:00")
    #asaTransferCriteria(city, "leśnica", "księże małe", "10:00:00")