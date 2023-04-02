from structures import PriorityQueue, findStopOfName, timeToTotal

def dijkstra(graph, start, end, departure_time):

    start_node = findStopOfName(graph, start)
    stop_node = findStopOfName(graph, end)
    time_total = timeToTotal(departure_time)

    q = PriorityQueue()
    q.put(start_node, 0)
    visited = set()

    tracker = {stop: ([], float('inf')) for stop in graph}
    # dict storing current best paths to a node, where:
    # first elem - path to node
    # second elem - path length
    tracker[start_node] = ([start_node], 0)

    while not q.empty():
        current_stop = q.get()

        if current_stop in visited:
            continue
        else:
            visited.add(current_stop)

        if current_stop == stop_node:
            tracker[current_stop] = ((tracker[current_stop][0] + [current_stop])[1:], tracker[current_stop][1])
            preetifyResult(tracker[current_stop], start_node, stop_node)
            return

        for departure in filter(lambda x: (x.departure_time>=time_total+tracker[current_stop][1]), current_stop.departures):
            # all departures that take place after (start departure time + time to get to current_stop)
            destination = findStopOfName(graph, departure.destination)

            #print(destination, tracker[destination], (tracker[current_stop][1] + departure.length))

            if destination.name == "wawrzyniaka":
                pass

            if not tracker[destination][0]:
                #print("ifnot")
                tracker[destination] = (tracker[current_stop][0] + [current_stop], tracker[current_stop][1] + departure.length)
            elif tracker[destination][1] > (tracker[current_stop][1] + departure.length):
                #print("elif")
                #print(tracker[destination][0] + [current_stop], tracker[destination][1] + departure.length)
                tracker[destination] = (tracker[destination][0] + [current_stop], tracker[destination][1] + departure.length)
            else:
                continue
            q.put(destination, tracker[destination][1])
            #print("\n")
    
    return


def preetifyResult(res, start, stop):
    stops, time = res
    result_str = ""
    for i, stop in enumerate(stops):
        result_str += stop.name
        if(i < len(stops) - 1):
            result_str += '-'
    print(f"Trasa od {start} do {stop}:")
    print(result_str)
    print(f"Zajmie {time}")