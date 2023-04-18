import pandas as pd
from collections import defaultdict
from structures import Stop
import pickle
import time

df = pd.read_csv('connection_graph.csv', index_col=0)
FILENAME = "graph.pkl"

def fetchNodes():
    stops_dict = defaultdict(set)
    print("Fetching nodes...")
    for _, elem in df.iterrows():
        stops_dict[elem['start_stop']].add(tuple(elem[6:8]))
        stops_dict[elem['end_stop']].add(tuple(elem[8:]))

    return list(sorted([Stop(stop[0], stop[1]) for stop in stops_dict.items()], key=lambda x: x.name))

def fetchEdges(graph):
    print("Fetching edges...")
    for _, elem in df.sort_values(by='start_stop').iterrows():
        for stop in graph:
            if stop.name==elem['start_stop'] and stop.name!=elem['end_stop']:
                stop.addDeparture(elem)
                break

def fetchLines():
    pass

def saveGraph(graph):
    print("Saving...")
    with open(FILENAME, "wb") as file:
        file.write(pickle.dumps(graph))

def readGraph():
    with open(FILENAME, "rb") as file:
        return pickle.loads(file.read())
    
def fullLoad():
    a = time.time()
    graph = fetchNodes()
    fetchEdges(graph)
    saveGraph(graph)
    print(f"Done in {time.time()-a}s!")