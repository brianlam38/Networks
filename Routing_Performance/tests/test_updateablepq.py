#!/usr/bin/python3
import pytest
from helpers.workload_queue import UpdateablePriorityQueue


@pytest.fixture
def q():
    hl = [(0, 'I'), (float('inf'), 'A'), (float('inf'), 'B'), (float('inf'),
                                                               'D'),
          (float('inf'), 'J'), (float('inf'), 'G'), (float('inf'),
                                                     'C'), (float('inf'), 'E'),
          (float('inf'), 'N'), (float('inf'), 'K'), (float('inf'),
                                                     'M'), (float('inf'), 'L'),
          (float('inf'), 'P'), (float('inf'), 'F'), (float('inf'),
                                                     'O'), (float('inf'), 'H')]

    return UpdateablePriorityQueue(hl)


@pytest.fixture
def q2():
    hl = [(0, 'I'), (float('inf'), 'A'), (float('inf'), 'B'), (float('inf'),
                                                               'D'),
          (float('inf'), 'J'), (float('inf'), 'G'), (float('inf'),
                                                     'C'), (float('inf'), 'E'),
          (float('inf'), 'N'), (float('inf'), 'K'), (float('inf'),
                                                     'M'), (float('inf'), 'L'),
          (float('inf'), 'P'), (float('inf'), 'F'), (float('inf'),
                                                     'O'), (float('inf'), 'H')]
    queue = UpdateablePriorityQueue([])
    for item_tuple in hl:
        queue.insert(item_tuple)
    return queue


def test_popinf(q, q2):
    for queue in [q, q2]:
        assert queue.pop() == (0, 'I')
        queue.update_priority((100, 'B'))
        queue.update_priority((5, 'J'))
        assert queue.pop() == (5, 'J')
        queue.update_priority((35, 'K'))
        queue.update_priority((55, 'L'))
        assert queue.pop() == (35, 'K')
        queue.update_priority((65, 'N'))
        assert queue.pop() == (55, 'L')
        queue.update_priority((85, 'M'))
        assert queue.pop() == (65, 'N')
        queue.update_priority((105, 'O'))
        queue.update_priority((77, 'M'))
        assert queue.pop() == (77, 'M')
        assert queue.pop() == (100, 'B')
