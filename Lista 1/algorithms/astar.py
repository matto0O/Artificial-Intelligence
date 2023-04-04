from structures import PriorityQueue, Stop, findStopOfName, timeToTotal, findDepartureBetween, toReadableTime
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

    print(f"Setup - {time.time() - computing_time_start}")
    computing_time_start = time.time()

    fullLoops = 0
    smallLoops = 0
    reconstruction = 0

    while not q.empty():
        computing_time_start = time.time()
        current_stop = q.get()

        if current_stop in visited:
            continue
        else:
            visited.add(current_stop)

        if current_stop == stop_node:
            rec = time.time()
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
            print(f"Recon {time.time()-rec}")
            print(f"small {smallLoops}")
            print(f"full {fullLoops}")
            #print(f"Czas wykonywania obliczeń - {time.time()-computing_time_start}s")
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

            smallLoops += time.time() - comp

        fullLoops += time.time() - computing_time_start
        computing_time_start = time.time()
    return


def preetifyResult(res):
    trip_time = 0
    print("=======================================================")
    for departure in res:
        trip_time += departure.length
        print(f"{departure.start.capitalize()} -> {departure.destination.capitalize()}, linia {departure.line}, odjazd o {toReadableTime(departure.departure_time)}, przyjazd o {toReadableTime(departure.arrival_time)}")
    print(f"Docierasz do przystanku o {toReadableTime(res[-1].arrival_time)} po {trip_time} minutach jazdy")
    print("=======================================================")


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

            transfer = departure.line not in (tracker[current_stop][3], None)
            if current_stop.name=="klimasa" and departure.destination=="transbud":
                pass
            
            if destination.name in [current_stop.name, tracker[current_stop][0]]:
                continue
            time_cost = departure.transferCriteria(time_total, transfer)
    
            if not tracker[destination][0] or time_cost < tracker[destination][1]:
                tracker[destination] = (current_stop, time_cost, departure.arrival_time, departure.line)
                q.put(destination, time_cost + current_stop.getHeuristic(destination))
    return