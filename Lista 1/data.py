import pandas as pd
from collections import defaultdict
from structures import Stop
import pickle

df = pd.read_csv('connection_graph.csv', index_col=0)
FILENAME = "graph.pkl"

def fetchNodes():
    stops_dict = defaultdict(set)
    print("Fetching nodes...")
    for _, elem in df.iterrows():
        stops_dict[elem['start_stop'].lower()].add(tuple(elem[6:8]))
        stops_dict[elem['end_stop'].lower()].add(tuple(elem[8:]))

    return [Stop(stop[0], stop[1]) for stop in stops_dict.items()]

def fetchEdges(graph):
    print("Fetching edges...")
    for _, elem in df.iterrows():
        [stop for stop in graph if stop.name==elem['start_stop'].lower()][0].addDeparture(elem)

def saveGraph(graph):
    print("Saving...")
    with open(FILENAME, "wb") as file:
        file.write(pickle.dumps(graph))

def readGraph():
    with open(FILENAME, "rb") as file:
        return pickle.loads(file.read())
    
def fullLoad():
    graph = fetchNodes()
    fetchEdges(graph)
    saveGraph(graph)
    print("Done!")