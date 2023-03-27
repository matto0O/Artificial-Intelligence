import pandas as pd
from collections import defaultdict
from structures import Stop
import pickle
from astar_algorithm import asa

df = pd.read_csv('connection_graph.csv', index_col=0)
city = list()

FILENAME = "graph.pkl"

def fetchNodes():
    stops_dict = defaultdict(set)
    print("Fetching nodes...")
    for _, elem in df.iterrows():
        stops_dict[elem['start_stop'].lower()].add(tuple(elem[6:8]))
        stops_dict[elem['end_stop'].lower()].add(tuple(elem[8:]))

    return [Stop(stop[0], stop[1]) for stop in stops_dict.items()]

def fetchEdges():
    print("Fetching edges...")
    for _, elem in df.iterrows():
        [stop for stop in city if stop.name==elem['start_stop'].lower()][0].addDeparture(elem)

def saveGraph():
    print("Saving...")
    with open(FILENAME, "wb") as file:
        file.write(pickle.dumps(city))

def readGraph():
    with open(FILENAME, "rb") as file:
        return pickle.loads(file.read())

if __name__=="__main__":
    # city = readGraph()
    # city = fetchNodes()
    # fetchEdges()
    # saveGraph()
    city = readGraph()
    asa(city, "krzyki", "racławicka")