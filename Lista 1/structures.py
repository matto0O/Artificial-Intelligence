import pandas as pd
import heapq
import time

def findDepartureBetween(start, stop, arrival):
    for departure in start.departures:
        if departure.destination==stop and departure.arrival_time==arrival:
            return departure
    exit(1)

def timeToTotal(time):
    split = time[:6].split(':')
    return int(split[0])*60 + int(split[1])

def toReadableTime(time):
    return f"{int(time/60)}:{str(time%60).zfill(2)}"

def findStopOfName(graph, node_name):
    for stop in graph:
        if stop.name==node_name:
            return stop
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
        self.start = info['start_stop'].lower()
        self.departure_time = timeToTotal(info['departure_time'])
        self.destination = info['end_stop'].lower()
        self.arrival_time = timeToTotal(info['arrival_time'])
        self.length = self.arrival_time - self.departure_time

    def __str__(self):
        return f"{self.line} odjeżdżające o {int(self.departure_time/60)}:{self.departure_time%60} z {self.start} dotrze do {self.destination} o {int(self.arrival_time/60)}:{self.arrival_time%60}"
    
    def __eq__(self, __o: object) -> bool:
        return self.line==__o.line and self.destination==__o.destination and self.departure_time==__o.d_time
    
    def timeCriteria(self, start_time):
        return self.arrival_time - start_time
    
    def transferCriteria(self, start_time, transfered):
        TRANSFER_THRESHOLD = 10
        return self.arrival_time - start_time + (TRANSFER_THRESHOLD if transfered else 0)

class Stop():
    """
    Node of a public transport graph, representing a group of stops (those holding the same name).
    -
    name - stop name\n
    posts - coordinates of all posts\ns
    departures - all of the departures from this group of stops
    """
    def __init__(self, name, posts):
        self.name = name.lower()
        self.posts = list(posts)
        self.departures = list()

    def __str__(self):
        return self.name
    
    def __repr__(self) -> str:
        return self.name

    def __eq__(self, __o: object):
        return self.name == str(__o)
    
    def __lt__(self, _):
        return self.__hash__

    def __hash__(self):
        return hash(self.name)
    
    def addDeparture(self, info:pd.Series):
        self.departures.append(Departure(info))
        
    def getHeuristic(self, end_stop):
        """
        Getter for heuristic value, using Manhattan Distance.\n
        Updates total f value.
        """
        MULTPLIER = 200
        this_x, this_y = self.posts[0]
        end_x, end_y = end_stop.posts[0]
        return MULTPLIER * (abs(this_x-end_x) + abs(this_y-end_y))

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return not self.elements

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]
