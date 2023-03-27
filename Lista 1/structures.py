import pandas as pd

def _timeToTotal(time):
    split = time[:6].split(':')
    return int(split[0])*60 + int(split[1])

class Departure():
    """
    Edge for the public transport graph, representing a route between two stops.
    -
    line - Symbol of a mean of public transport\n
    d_time - Departure time in minutes (7:30AM -> 450)\n
    a_time - Arrival time in minutes\n
    destination - Name of the destination stop
    """
    def __init__(self, info: pd.Series):
        self.line:str = info['line']
        self.d_time = _timeToTotal(info['departure_time'])
        self.destination = info['end_stop'].lower()
        self.a_time = _timeToTotal(info['arrival_time'])

    def __str__(self):
        return f"{self.line} odjeżdżające o {int(self.d_time/60)}:{self.d_time%60} dotrze do {self.destination} o {int(self.a_time/60)}:{self.a_time%60}"
    
    def deltaTime(self):
        """
        Time length of a ride in minutes
        """
        return self.a_time - self.d_time

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

    def __str__(self):
        return self.name

    def __eq__(self, __o: object):
        return self.name == str(__o)
    
    def addDeparture(self, info:pd.Series):
        self.departures.append(Departure(info))
        
    def manhattanDistance(self, end_stop):
        this_x, this_y = self.posts[0]
        end_x, end_y = end_stop.posts[0]
        return abs(this_x-end_x) + abs(this_y-end_y)

