def findStopOfName(graph, node_name):
    try:
        return [stop for stop in graph if stop.name==node_name.lower()][0]
    except IndexError:
        print("Nie ma takiego przystanku")
        exit(0)

def findWrapperByName(graph, node_name):
    try:
        return [stop for stop in graph if stop.obj.name==node_name.lower()][0]
    except IndexError:
        print("Nie ma takiego przystanku")
        exit(0)

def asa(graph_stale, start_name, end_name, start_time):
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

    # # assigning distance to the end
    # graph = [NodeWrapper(stop, destination) for stop in graph_stale]

    # # adding starting stop onto the open list
    # start = findStopOfName(graph_stale, start_name)
    # open.append(NodeWrapper(start, destination))
    
    # while len(open)>0:
    #     # finiding lowest f value stop
    #     current = sorted(open, key=lambda x: x.f).pop(0)[0]

    #     # path was found
    #     if str(current)==destination:
    #         print("found")
    #         # TODO implement returning the path
    #         return
        
    #     closed.append(current)

    #     neighbors = [findWrapperByName(graph, departure.destination) 
    #                  for departure in current.obj.departures]
        
    #     for neighbor in neighbors:
    #         if neighbor in closed:
    #             continue
    #         neighbor_departure = [departure for departure in current.obj.departure if departure.]
    #         neighbor.setG(current.g + [departure.deltaTime for departure in current.obj.departures])
