from data import fullLoad, readGraph
from algorithms.dijkstra import dijkstra
from algorithms.astar import asaTimeCriteria, asaTransferCriteria

if __name__=="__main__":
    #fullLoad()
    city = readGraph()
    # dijkstra(city, "Kamienna", "Kopańskiego", "9:55:00")
    asaTimeCriteria(city, "LEŚNICA", "KSIĘŻE MAŁE", "10:00:00")
    # asaTimeCriteria(city, "Kamienna", "Kopańskiego", "9:55:00")
    # print("\n")
    # asaTimeCriteria(city, "LEŚNICA", "KSIĘŻE MAŁE", "10:00:00")
    # print("\n")
    # asaTimeCriteria(city, "TARNOGAJ", "Wapienna", "10:00:00")