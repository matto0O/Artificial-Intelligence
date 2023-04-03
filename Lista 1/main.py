from data import fullLoad, readGraph
from algorithms.dijkstra import dijkstra
import gpt
import datetime

if __name__=="__main__":
    city = readGraph()
    #asa(city, "krzyki", "racławicka")
    dijkstra(city, "leśnica", "księże małe", "10:00:00")
    #gpt.dijkstra(gpt.create_graph("connection_graph.csv"),"TARNOGAJ", "Most Grunwaldzki", datetime.time(hour=9, minute=30, second=0))