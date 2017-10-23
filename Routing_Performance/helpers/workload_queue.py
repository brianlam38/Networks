import heapq
import warnings
from helpers.virtual_connection import VirtualConnection
from collections import namedtuple

# defines tuple used in WorkloadQueue - has time, VirtualConnection instance
WorkloadTuple = namedtuple('WorkloadTuple', 'time, connection')


class WorkloadQueue:
    def __init__(self, workload_file_path):
        workload_tuple_list = self.parse_workload(workload_file_path)
        self.queue = UpdateablePriorityQueue(workload_tuple_list)

    def add(self, connection_tuple):
        # add virtual connection and sort as you go
        self.queue.insert(connection_tuple)

    def pop(self):
        return self.queue.pop()

    def parse_workload(self, file_path):
        # NOTE: add in cleanup connections at duration on the fly IF connection succeeds
        # Only parses initial workload
        # return list of tuple in form of (time to deal, virtualconnection)
        f = open(file_path, "r")
        data = f.readlines()
        result = []
        for line in data:
            line = line.split()
            time_start = float(line[0])
            src = line[1]
            dest = line[2]
            duration = float(line[3])
            result.append(
                WorkloadTuple(
                    time=time_start,
                    connection=VirtualConnection(time_start, src, dest,
                                                 duration)))
        return result

    def peek_final_connection(self):
        return self.queue.peek_largest(1)[0]

    def peek_duration(self):
        return self.queue.peek_largest(1)[0].time

    def is_empty(self):
        return self.queue.is_empty()


class UpdateablePriorityQueue:
    """
    Priority Queue using Min Heap (heapq library), with updateable priorities
    after insertion
    Assume unique items; will throw warning if duplicate is added.
    Duplicates are both updated if found
    NOTE: make sure item_tuples in a queue is always in form of (priority, item)
    """

    def __init__(self, init_list):
        self.heap_list = init_list
        heapq.heapify(self.heap_list)

    def __len__(self):
        return len(self.heap_list)

    def __contains__(self, vertex):
        for item_tuple in self.heap_list:
            if item_tuple[1] == vertex:
                return True
        return False

    # input in (priority, item)
    def insert(self, item_tuple):
        if (item_tuple in self.heap_list):
            warnings.warn(
                "tuple already exists; any updates will update both iterations",
                UserWarning)
        heapq.heappush(self.heap_list, item_tuple)

    def pop(self):
        return heapq.heappop(self.heap_list)

    # input in (priority, item)
    def update_priority(self, item_tuple):
        if len(item_tuple) > 2 and isinstance(
                item_tuple[0], int) and isinstance(item_tuple[1], str):
            raise AttributeError('expected tuple in the form (item, value)')
        update_flag = False
        for t in self.heap_list:
            if t[1] == item_tuple[1]:
                self.heap_list.remove(t)
                heapq.heapify(self.heap_list)
                self.insert(item_tuple)
                update_flag = True
        if not update_flag:
            warnings.warn("tuple not found - no update made", UserWarning)

    def peek_largest(self, n):
        return heapq.nlargest(n, self.heap_list)

    def is_empty(self):
        return len(self.heap_list) == 0
