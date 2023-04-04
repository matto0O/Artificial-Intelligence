from structures import PriorityQueue, Stop, findStopOfName, timeToTotal, findDepartureBetween, preetifyResult
import time

def asaTimeCriteria(graph, start, end, departure_time):
    """
    Implementation of an A* Algorithm using time criteria
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

    tracker = {stop: (Stop, float('inf'), int) for stop in graph}
    # dict storing current best paths to a node, where:
    # first elem - path to node
    # second elem - path length
    tracker[start_node] = (None, 0, time_total)

    while not q.empty():
        current_stop = q.get()

        if current_stop in visited:
            continue
        else:
            visited.add(current_stop)

        if current_stop == stop_node:
            # path reconstruction
            stopA = tracker[current_stop][0]
            stopB = current_stop
            departures = []
            while stopA != start_node:
                departures.append(findDepartureBetween(stopA, stopB, tracker[stopB][2]))
                stopA, stopB = tracker[stopA][0], stopA
            departures.append(findDepartureBetween(stopA, stopB, tracker[stopB][2]))
            departures.reverse()
            preetifyResult(departures)
            print(f"Czas wykonywania obliczeń - {time.time()-computing_time_start}s")
            return

        for departure in filter(lambda x: (x.departure_time>=tracker[current_stop][2]), current_stop.departures):
            comp = time.time()
            # all departures that take place after current_stop arrival time
            destination = findStopOfName(graph, departure.destination)
            if destination.name in [current_stop.name, tracker[current_stop][0]]:
                continue
            time_cost = departure.timeCriteria(time_total)

            if not tracker[destination][0] or time_cost < tracker[destination][1]:
                tracker[destination] = (current_stop, time_cost, departure.arrival_time)
                q.put(destination, time_cost + current_stop.getHeuristic(destination))
    return

def asaTransferCriteria(graph, start, end, departure_time):
    """
    Implementation of an A* Algorithm using time criteria
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
    tracker[start_node] = (None, 0, time_total, None)

    while not q.empty():
        current_stop = q.get()
        current_time = time_total

        if current_stop in visited:
            continue
        else:
            visited.add(current_stop)

        if current_stop == stop_node:
            # path reconstruction
            stopA = tracker[current_stop][0]
            stopB = current_stop
            departures = []
            while stopA != start_node:
                departures.append(findDepartureBetween(stopA, stopB, tracker[stopB][2]))
                stopA, stopB = tracker[stopA][0], stopA
            departures.append(findDepartureBetween(stopA, stopB, tracker[stopB][2]))
            departures.reverse()
            preetifyResult(departures)
            print(f"Czas wykonywania obliczeń - {time.time()-computing_time_start}s")
            return

        for departure in filter(lambda x: (x.departure_time>=tracker[current_stop][2]), current_stop.departures):
            # all departures that take place after current_stop arrival time
            destination = findStopOfName(graph, departure.destination)

            transfer = departure.line != tracker[current_stop][3]
            
            if destination.name in [current_stop.name, tracker[current_stop][0]]:
                continue
            time_cost = departure.transferCriteria(current_time, transfer)
    
            if not tracker[destination][0] or time_cost < tracker[destination][1]:
                tracker[destination] = (current_stop, time_cost, departure.arrival_time, departure.line)
                q.put(destination, time_cost + current_stop.getHeuristic(destination))
        current_time += tracker[current_stop][1]
    return