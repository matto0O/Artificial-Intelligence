from structures import *
import time

def dijkstra(graph, start, end, departure_time):
    """
    Implementation of a Dijkstra algorithm
    -
    graph - graph used to browse for an optimal route\n
    start - starting stop name\n
    end - end goal\n
    departure_time - the earliest time to hop onto a bus/tram
    """
    computing_time_start = time.time()

    start_node = findStopOfName(graph, start)
    stop_node = findStopOfName(graph, end)
    time_total = timeToTotal(departure_time)

    q = PriorityQueue()
    q.put(start_node, 0)
    visited = set()

    tracker = {stop: (Stop, float('inf'), int, str) for stop in graph}
    # dict storing current best paths to a node, where:
    # first elem - path to node
    # second elem - path length
    # third elem - arrival time
    # fourth elem - line
    tracker[start_node] = (None, 0, time_total, None)

    while not q.empty():
        current_stop = q.get()

        if current_stop in visited:
            continue
        else:
            visited.add(current_stop)

        if current_stop == stop_node:
            # path reconstruction
            stopB = current_stop
            tracker = checkForTransferAvoidance(tracker, stopB, start)
            stopA = tracker[current_stop][0]
            departures = []
            while stopA != start_node:
                departures.append(findDepartureBetweenOfLine(stopA, stopB, tracker[stopB][3], tracker[stopB][2]))
                stopA, stopB = tracker[stopA][0], stopA
            departures.append(findDepartureBetweenOfLine(stopA, stopB, tracker[stopB][3], tracker[stopB][2]))
            departures.reverse()
            preetifyResult(departures)
            print(f"Czas wykonywania obliczeń - {time.time()-computing_time_start}s")
            return
        
        collection = sorted(filter(lambda x: (x.departure_time>=tracker[current_stop][2]), current_stop.departures), key=lambda x: x.departure_time)

        checked_departures = set()

        for departure in collection:
            # all departures that take place after current_stop arrival time
            x = (departure.line, departure.destination)
            if x not in checked_departures:
                checked_departures.add(x)
                destination = findStopOfName(graph, departure.destination)

                transfer = departure.line != tracker[current_stop][3]

                if destination.name not in [current_stop.name, tracker[current_stop][0]]:
                    time_cost = departure.timeCriteria(time_total, transfer)

                    if not tracker[destination][0] or time_cost < tracker[destination][1]:
                        tracker[destination] = (current_stop, time_cost, departure.arrival_time, departure.line)
                        q.put(destination, time_cost)
    return