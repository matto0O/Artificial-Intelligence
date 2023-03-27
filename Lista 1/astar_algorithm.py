def findStopOfName(graph, node_name):
    try:
        return [stop for stop in graph if stop.name==node_name.lower()][0]
    except IndexError:
        print("Nie ma takiego przystanku")
        exit(0)


def asa(graph_stale, start_name, end_name):
    """
    Implementation of an A* Algorithm
    -
    graph_stale - graph used to browse for an optimal route\n
    start_name - starting stop name\n
    end_name - end goal
    """
    open = list()
    closed = list()
    destination = findStopOfName(graph_stale, end_name.lower())

    # assigning distance to the end
    graph = [(stop, stop.manhattanDistance(destination)) for stop in graph_stale]

    open.append((findStopOfName(graph,start_name),f))
    
    while len(open)>0:
        elem = sorted(open, key=lambda x: x[1]).pop(0)[0]
        if str(elem)==destination:
            print("found")
            return
        successors = [(findStopOfName(graph, depart.destination), depart.deltaTime())
                       for depart in elem.departures]
        for successor in successors:
            pass
