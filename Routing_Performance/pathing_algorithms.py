from helpers.workload_queue import UpdateablePriorityQueue
import random as r
# Random parameters used in RNG for breaking ties below
r.seed()  # use system time as seed
tie_break_chance = 0.5


def shortest_path(graph, source, dest, path_type='SDP'):
    """
    Find shortest path to dest node from source using 3 path_types:
    Shortest Hop Path, Shortest Delay Path and Least Loaded Path
    (specify with path_type)
    Calculates dist{v} - holds minimum distance to each v
    Follow chain of prev{v} to generate shortest path to dest node v

    Base Pseudocode Source: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """
    vertices = UpdateablePriorityQueue([])
    dist = {}
    prev = {}
    for vertex in graph.nodes:
        dist[vertex] = float('inf')
        prev[vertex] = None  # set previous for a vertex when possible
        vertices.insert((dist[vertex], vertex))
    dist[source] = 0
    vertices.update_priority((dist[source], source))
    while len(vertices) > 0:
        # take lowest valued entries first; tuple (vertex, dist[vertex])
        u_cur_delay, u = vertices.pop()
        for neighbour_v in graph.edges[u]:
            if neighbour_v not in vertices:
                continue  # skip stuff not in queue anymore
            # in SHP, all delays are 1 (only counting link hops)
            if path_type == 'SHP':
                added_delay = 1
                altered_delay = u_cur_delay + added_delay
            elif path_type == 'SDP':
                added_delay = graph.delays[(u, neighbour_v)]
                altered_delay = u_cur_delay + added_delay
            elif path_type == 'LLP':
                # altered_delay = (len(graph.virtual_connections)) / (graph.cap[(
                #    u, neighbour_v)])
                active_connections = graph.max_cap[(
                    u, neighbour_v)] - graph.cap[(u, neighbour_v)]
                calc_delay = (active_connections) / (graph.max_cap[(
                    u, neighbour_v)])
                # update the maximum load on this current path - first one will be zero
                altered_delay = max(calc_delay, u_cur_delay)
                # altered_delay = calc_delay
            else:
                raise ValueError(
                    "Invalid value for path_type to shortest_path")
            # if new altered cost is less than a current minimum dist TO a neighbour, update
            if altered_delay <= dist[neighbour_v]:
                if altered_delay == dist[neighbour_v] and r.random(
                ) < tie_break_chance:
                    continue  # randomly allow alternate path with equal cost to break tie
                dist[neighbour_v] = altered_delay
                prev[neighbour_v] = u
                vertices.update_priority((dist[neighbour_v], neighbour_v))
    return get_path_dist_tuple(dist, prev, dest)


def get_path_dist_tuple(distance_dict, prev_node_dict, dest):
    # calculate path, cost from source to dest:
    u = dest
    path = []
    while u is not None:
        path.insert(0, u)
        u = prev_node_dict[u]
    return (path, distance_dict[dest])
