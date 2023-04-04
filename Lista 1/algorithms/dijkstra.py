from structures import PriorityQueue, findStopOfName, timeToTotal, findDepartureBetween, toReadableTime, Stop, Departure

def dijkstra(graph, start, end, departure_time):

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
            return

        for departure in filter(lambda x: (x.departure_time>=tracker[current_stop][2]), current_stop.departures):
            # all departures that take place after current_stop arrival time
            destination = findStopOfName(graph, departure.destination)
            if destination.name in [current_stop.name, tracker[current_stop][0]]:
                continue
            time_cost = departure.timeCriteria(time_total)

            if not tracker[destination][0] or time_cost < tracker[destination][1]:
                tracker[destination] = (current_stop, time_cost, departure.arrival_time)
                q.put(destination, time_cost)
    return


def preetifyResult(res):
    trip_time = 0
    print("=======================================================")
    for departure in res:
        trip_time += departure.length
        print(f"{departure.start.capitalize()} -> {departure.destination.capitalize()}, linia {departure.line}, odjazd o {toReadableTime(departure.departure_time)}, przyjazd o {toReadableTime(departure.arrival_time)}")
    print(f"Docierasz do przystanku o {toReadableTime(res[-1].arrival_time)} po {trip_time} minutach jazdy")
    print("=======================================================")