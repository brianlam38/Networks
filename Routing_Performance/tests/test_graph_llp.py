#!/usr/bin/python3
from helpers.pathing_algorithms import shortest_path
from helpers.virtual_connection import VirtualConnection


def test_llp_topology_simple(graph_topology_simple):
    v = VirtualConnection(0, 'A', 'D', 1)
    success = v.fill_path(graph_topology_simple, shortest_path, 'SDP')
    assert success is True
    assert v.path == ['A', 'C', 'D']
    v = VirtualConnection(0, 'B', 'C', 1)
    success = v.fill_path(graph_topology_simple, shortest_path, 'SDP')
    assert success is True
    assert v.path == ['B', 'C']
    v = VirtualConnection(0, 'B', 'D', 1)
    success = v.fill_path(graph_topology_simple, shortest_path, 'SDP')
    assert v.path == ['B', 'C', 'D']
    v = VirtualConnection(0, 'A', 'D', 1)
    success = v.fill_path(graph_topology_simple, shortest_path, 'LLP')
    assert success is True
    assert v.path == ['A', 'B', 'D']
