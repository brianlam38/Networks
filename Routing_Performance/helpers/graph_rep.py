from collections import defaultdict


class Graph:
    """
    Adjacency list Graph Representation
    """

    def __init__(self):
        self.nodes = set()  # switches/routers
        self.edges = defaultdict(list)  # links
        self.delays = {}  # link delays
        self.cap = {}  # circuit capacity
        self.max_cap = {}  # max circuit capacity
        self.virtual_connections = set()
        self.debug = False

    # add a new switch/router
    def add_node(self, node):
        self.nodes.add(node)

    # add a new link
    # !neighbour = infinite delay
    def add_edge(self, from_n, to_n, delay, capacity):
        # init link
        self.edges[from_n].append(to_n)
        self.edges[to_n].append(from_n)
        # init link delay
        self.delays[(from_n, to_n)] = delay
        self.delays[(to_n, from_n)] = delay
        # init link capacity - this one can change
        self.cap[(from_n, to_n)] = capacity
        self.cap[(to_n, from_n)] = capacity
        self.max_cap[(from_n, to_n)] = capacity
        self.max_cap[(to_n, from_n)] = capacity

    def add_connection(self, connection):
        connection_edges = self.path_list_to_edges(connection.path)
        for edge_tuple in connection_edges:
            reverse_tuple = (edge_tuple[1], edge_tuple[0])
            if self.cap[edge_tuple] < 1 or self.cap[reverse_tuple] < 1:
                return False
        # reached here: success
        for edge_tuple in connection_edges:
            reverse_tuple = (edge_tuple[1], edge_tuple[0])
            self.cap[edge_tuple] -= 1
            self.cap[reverse_tuple] -= 1
        self.virtual_connections.add(connection)  # add virtual connection
        if self.debug:
            print(
                """Just added connection with path: {} start: {} duration: {}, end: {}\n
                edges: {}, new capacities: {}
                """
                .format(connection.path, connection.start, connection.duration,
                        connection.start + connection.duration,
                        self.path_list_to_edges(connection.path),
                        self.get_edge_list_capacities(
                            self.path_list_to_edges(connection.path))))
        return True

    def remove_connection(self, connection):
        if connection not in self.virtual_connections:
            return False
        connection_edges = self.path_list_to_edges(connection.path)
        for edge_tuple in connection_edges:
            reverse_tuple = (edge_tuple[1], edge_tuple[0])
            self.cap[edge_tuple] += 1
            self.cap[reverse_tuple] += 1
        try:
            self.virtual_connections.remove(connection)
        except:
            raise ValueError("tried to remove a connection not in graph")
        if self.debug:
            print(
                """Just removed connection with path: {} start: {} duration: {}, end: {}\n
                edges: {}, new capacities: {}
                """
                .format(connection.path, connection.start, connection.duration,
                        connection.start + connection.duration,
                        self.path_list_to_edges(connection.path),
                        self.get_edge_list_capacities(
                            self.path_list_to_edges(connection.path))))
        return True

    def path_list_to_edges(self, path):
        """convert to list of edge tuples (from_n, to_n), helper for above methods
        nEdges = nNodes - 1
        [a, b, c, d]
        [(A,B), B,C ]..
        """
        # 1.
        nodes = iter(path)
        edges = []
        from_node = None
        try:
            for node in nodes:
                if from_node is None:
                    from_node = node
                    to_node = next(nodes)
                else:
                    from_node = to_node
                    to_node = node
                edges.append((from_node, to_node))
        except StopIteration:
            raise ValueError("Attempt to convert empty path to edges")
        return edges

    def get_edge_list_delays(self, edge_list):
        """
        Input: list of tuples (from_n, to_n)
        Return list of delays corresponding to each tuple
        """
        result = []
        for edge_tuple in edge_list:
            result.append(self.delays[edge_tuple])
        return result

    def get_edge_list_capacities(self, edge_list):
        #3.
        result = []
        for edge_tuple in edge_list:
            result.append(self.cap[edge_tuple])
        return result

    def parse_topology(self, file_path):
        f = open(file_path, "r")
        data = f.readlines()
        for line in data:
            line = line.split()
            x = line[0]
            y = line[1]
            delay = line[2]
            cap = line[3]
            self.add_node(x)
            self.add_node(y)
            self.add_edge(x, y, int(delay), int(cap))

    def show_graph(self):
        """display graph nodes, links, link delay values, link capacity, curr link load"""
        for n in self.nodes:
            print("router = {}".format(n))
            for e in self.edges[n]:
                print("nb: {} | delay: {} | capacity: {} | max capacity: {}" \
                .format(e, self.delays[(n, e)], self.cap[(n, e)], self.max_cap[(n, e)]))
            print("-----------------")
