import pandas as pd

def timeToTotal(time):
    split = time[:6].split(':')
    return int(split[0])*60 + int(split[1])

def findStopOfName(graph, node_name):
    try:
        return [stop for stop in graph if stop.name==node_name.lower()][0]
    except IndexError:
        print("Nie ma takiego przystanku")
        exit(0)

class Departure():
    """
    Edge for the public transport graph, representing a route between two stops.
    -
    line - Symbol of a mean of public transport\n
    departure_time - Departure time in minutes (7:30AM -> 450)\n
    arrival_time - Arrival time in minutes\n
    start - Name of the stop where the line departs\n
    destination - Name of the destination stop\n
    length - Travel time in minutes
    """
    def __init__(self, info: pd.Series):
        self.line:str = info['line']
        self.start = info['start_stop'].lower().capitalize()
        self.departure_time = timeToTotal(info['departure_time'])
        self.destination = info['end_stop'].lower().capitalize()
        self.arrival_time = timeToTotal(info['arrival_time'])
        self.length = self.arrival_time - self.departure_time

    def __str__(self):
        return f"{self.line} odjeżdżające o {int(self.departure_time/60)}:{self.departure_time%60} z {self.start} dotrze do {self.destination} o {int(self.arrival_time/60)}:{self.arrival_time%60}"
    
    def __eq__(self, __o: object) -> bool:
        return self.line==__o.line and self.destination==__o.destination and self.departure_time==__o.d_time

class Stop():
    """
    Node of a public transport graph, representing a group of stops (those holding the same name).
    -
    name - stop name\n
    posts - coordinates of all posts\n
    departures - all of the departures from this group of stops
    """
    def __init__(self, name, posts):
        self.name = name
        self.posts = list(posts)
        self.departures = list()
        self.g = self.h = self.f = 0

    def __str__(self):
        return self.name

    def __eq__(self, __o: object):
        return self.name == str(__o)
    
    def __hash__(self):
        return hash(self.name)
    
    def addDeparture(self, info:pd.Series):
        self.departures.append(Departure(info))
        
    def setHeuristic(self, end_stop):
        """
        Setter for heuristic value, using Manhattan Distance.\n
        Updates total f value.
        """
        this_x, this_y = self.posts[0]
        end_x, end_y = end_stop.posts[0]
        self.h = abs(this_x-end_x) + abs(this_y-end_y)
        self.f = self.h + self.g

    def setG(self, g):
        """
        Setter for graph related value.\n
        Updates total f value.
        """
        self.g = g
        self.f = self.g + self.h

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item, priority):
        self.elements.append((item,priority))

    def get(self):
        self.elements.sort(key=lambda x:x[1])
        return self.elements.pop(0)[0]