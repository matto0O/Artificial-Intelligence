from structures import PriorityQueue, findStopOfName, timeToTotal, findDepartureBetween, Stop, Departure

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
            #preetifyResult(tracker[current_stop], start_node, stop_node)
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


def preetifyResult(res, start, stop):
    print(res)
    # last_stop, time, departure = res
    # result_str = ""
    # for i, stop in enumerate(last_stop):
    #     result_str += stop.name
    #     if(i < len(last_stop) - 1):
    #         result_str += '-'
    # print(f"Trasa od {start} do {stop}:")
    # print(result_str)
    # print(f"Zajmie {time}")    