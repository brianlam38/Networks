#!/usr/bin/python3
from helpers.pathing_algorithms import shortest_path


def test_shortest_hop_path(graph):
    result_path, result_hops = shortest_path(graph, 'a', 'i', path_type='SHP')
    assert result_path == ['a', 'e', 'i']
    assert result_hops == 2

def test_shortest_hop_txt_topology_simple(graph_topology_simple):
    result_path, result_hops = shortest_path(
        graph_topology_simple, 'A', 'D', path_type='SHP')
    assert result_path == ['A', 'B', 'D'] or result_path == ['A', 'C', 'D']
    assert result_hops == 2

def test_shortest_hop_txt_topology(graph_topology):
    result_path, result_hops = shortest_path(
        graph_topology, 'D', 'N', path_type='SHP')
    assert result_path == ['D', 'F', 'O', 'N']
    assert result_hops == 3
    result_path, result_hops = shortest_path(
        graph_topology, 'I', 'H', path_type='SHP')
    assert result_path == ['I', 'B', 'A', 'H']
    assert result_hops == 3
    result_path, result_delays = shortest_path(
        graph_topology, 'A', 'O', path_type='SHP')
    assert result_path == ['A', 'H', 'G', 'O'
                           ] or result_path == ['A', 'H', 'F', 'O']
    assert result_hops == 3

# def test_shortest_hop_path_brian(graph):
#     result_path, result_hops = shortest_hop_mst(graph, 'a', 'i')
#     assert result_path == ['a', 'e', 'i']
#     assert result_hops == 2

# def test_shortest_hop_txt_topology_simple_brian(graph_topology_simple):
#     result_path, result_hops = shortest_hop_mst(graph_topology_simple, 'A',
#                                                 'D')
#     # should be random choice between these 2
#     assert result_path == ['A', 'B', 'D'] or result_path == ['A', 'C', 'D']
#     assert result_hops == 2


# def test_shortest_hop_txt_topology_brian(graph_topology):
#     result_path, result_hops = shortest_hop_mst(graph_topology, 'D', 'N')
#     assert result_path == ['D', 'F', 'O', 'N']
#     assert result_hops == 3
#     result_path, result_hops = shortest_hop_mst(graph_topology, 'I', 'H')
#     assert result_path == ['I', 'B', 'A', 'H']
#     assert result_hops == 3
#     result_path, result_delays = shortest_hop_mst(graph_topology, 'A', 'O')
#     assert result_path == ['A', 'H', 'G', 'O'
#                            ] or result_path == ['A', 'H', 'F', 'O']
#     assert result_hops == 3


