import pytest
import copy

from helpers.virtual_connection import VirtualConnection


def test_path_to_edge_tuples(graph, graph_topology, graph_topology_simple):
    assert_path_edges(graph, ['a', 'c', 'd', 'g', 'i'],
                      [('a', 'c'), ('c', 'd'), ('d', 'g'), ('g', 'i')])
    assert_path_edges(graph, ['a', 'e', 'i'], [('a', 'e'), ('e', 'i')])
    assert_path_edges(graph_topology_simple, ['A', 'C', 'D'], [('A', 'C'),
                                                               ('C', 'D')])
    assert_path_edges(graph_topology_simple, ['B', 'C'], [('B', 'C')])
    assert_path_edges(graph_topology_simple, ['B', 'C', 'D'], [('B', 'C'),
                                                               ('C', 'D')])
    assert_path_edges(graph_topology_simple, ['A', 'B', 'D'], [('A', 'B'),
                                                               ('B', 'D')])
    assert_path_edges(graph_topology, ['D', 'F', 'P', 'O', 'N'],
                      [('D', 'F'), ('F', 'P'), ('P', 'O'), ('O', 'N')])
    assert_path_edges(graph_topology, ['I', 'J', 'K', 'N', 'O', 'G', 'H'],
                      [('I', 'J'), ('J', 'K'), ('K', 'N'), ('N', 'O'),
                       ('O', 'G'), ('G', 'H')])
    assert_path_edges(graph_topology, ['A', 'B', 'I', 'J', 'K', 'N', 'O'],
                      [('A', 'B'), ('B', 'I'), ('I', 'J'), ('J', 'K'),
                       ('K', 'N'), ('N', 'O')])
    assert_path_edges(graph_topology, ['B', 'A', 'C', 'D', 'F'],
                      [('B', 'A'), ('A', 'C'), ('C', 'D'), ('D', 'F')])


def test_connections(graph):
    add_then_remove_test(graph, ['a', 'c', 'd', 'g', 'i'], [1, 1, 1, 1],
                         [3, 1, 2, 2])
    add_then_remove_test(graph, ['a', 'e', 'i'], [1, 1], [2, 7])


def test_connections_topology_simple(graph_topology_simple):
    add_then_remove_test(graph_topology_simple, ['B', 'C'], [20], [20])
    add_then_remove_test(graph_topology_simple, ['B', 'C', 'D'], [20, 20],
                         [20, 8])
    add_then_remove_test(graph_topology_simple, ['A', 'B', 'D'], [19, 70],
                         [10, 30])


def test_connections_topology_complex(graph_topology):
    add_then_remove_test(graph_topology, ['D', 'F', 'P', 'O', 'N'],
                         [20, 27, 36, 50], [100, 30, 10, 40])
    add_then_remove_test(graph_topology, ['I', 'J', 'K', 'N', 'O', 'G', 'H'],
                         [35, 36, 45, 50, 25, 20], [5, 30, 30, 40, 40, 100])
    add_then_remove_test(graph_topology, ['A', 'B', 'I', 'J', 'K', 'N', 'O'],
                         [20, 32, 35, 36, 45, 50], [30, 100, 5, 30, 30, 40])
    add_n_times_test(graph_topology, ['D', 'F', 'P', 'O', 'N'],
                     [20, 27, 36, 50], [100, 30, 10, 40], 20)
    add_n_times_test(
        graph_topology, ['D', 'F', 'P', 'O', 'N'], [20, 27, 36, 50],
        [100, 30, 10, 40],
        21,
        status=False)


def add_then_remove_test(graph, path, prior_cap_list, path_delays,
                         status=True):
    conn = VirtualConnection(0, path[0], path[len(path) - 1], 1)
    conn.path = path
    connection_edges = graph.path_list_to_edges(conn.path)
    assert graph.get_edge_list_capacities(connection_edges) == prior_cap_list
    success = graph.add_connection(conn)
    assert success == status
    if success is True:
        post_cap_list = [(x - 1) for x in prior_cap_list]
        assert graph.get_edge_list_capacities(
            connection_edges) == post_cap_list
    assert graph.get_edge_list_delays(connection_edges) == path_delays
    success = graph.remove_connection(conn)
    assert success == status
    assert graph.get_edge_list_capacities(connection_edges) == prior_cap_list


def add_n_times_test(graph, path, prior_cap_list, path_delays, n, status=True):
    graph_clone = copy.deepcopy(graph)
    conn = VirtualConnection(0, path[0], path[len(path) - 1], 1)
    conn.path = path
    connection_edges = graph_clone.path_list_to_edges(conn.path)
    assert graph_clone.get_edge_list_capacities(
        connection_edges) == prior_cap_list
    assert graph_clone.get_edge_list_delays(connection_edges) == path_delays
    i = 0
    while i < n:
        success = graph_clone.add_connection(conn)
        if success is True:
            post_cap_list = [(x - 1) for x in prior_cap_list]
            assert graph_clone.get_edge_list_capacities(
                connection_edges) == post_cap_list
            prior_cap_list = post_cap_list  # update for next loop
            i += 1
        elif success is False and status is True:
            return False
        elif success is False and status is False:
            return True
    return True


def assert_path_edges(graph, path, edges):
    assert graph.path_list_to_edges(path) == edges
    assert (len(graph.path_list_to_edges(path))) == len(path) - 1
