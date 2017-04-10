from networkx import *


class FA:
    """
    Base class for any finite automata

    Contains the basic data structures & functions any FA should have
    """
    epsilon = '\u03B5'

    def __init__(self):
        self.node_index = 0
        self.states = []
        self.graph = MultiDiGraph()

    def move(self, source, input):
        """
        Move function, takes source node(s) and input.
        Moves from source under input through the graph
        :param source: source node(s) [integer]
        :param input: input literal [character]
        :return: the destination nodes (states)
        """
        # raise NotImplementedError
        destination = set()

        nodes = {source} if not isinstance(source, set) else source
        nodes.update(self.get_epsilon_closures(nodes))
        inputs = {input} if not isinstance(input, set) else input

        for node in nodes:
            for edge in self.graph.edges_iter(node, True):
                from_node, to_node, weight = edge
                weight = weight['weight']
                try:
                    weight = weight if weight == FA.epsilon else eval(weight)
                except TypeError:
                    weight = str(chr(weight))

                for input in inputs:
                    if weight == str(input):
                        destination.add(to_node)

        destination.update(self.get_epsilon_closures(destination))
        return destination

    def get_node_index(self):
        """
        :return: current node index
        """
        return self.node_index

    def increment_node_index(self):
        """
        increments node index

        this was separated from the `get_node_index` function, since
            it is not always required after
        """
        self.node_index += 1

    def __epsilon_closure(self, node):
        """
        calculates the epsilon closures of a given state.
        the epsilon closure is given by the set of states to which transitioning
        to them doesn't have a cost (zero weight)

        :param node: any given node in an FA
        :return: set of epsilon closures
        """
        epsilon_closure = {node}

        node_neighbors = self.graph.neighbors(node)
        for neighbor in node_neighbors:
            edge = self.graph.get_edge_data(node, neighbor)
            weight = edge['weight']

            if weight == FA.epsilon:
                epsilon_closure.add(neighbor)

        return epsilon_closure

    def get_epsilon_closures(self, nodes):
        """
        Applies __epsilon_closure() recursively to detect all epsilon closures
        of given nodes
        """
        nodes = {nodes} if not isinstance(nodes, set) else nodes
        epsilon_closures = set()

        for node in nodes:
            for epsilon_node in self.__epsilon_closure(node):
                if epsilon_node not in nodes:
                    epsilon_closures.add(epsilon_node)

        if not epsilon_closures:
            return nodes

        nodes.update(epsilon_closures)
        return self.get_epsilon_closures(nodes)

    def draw(self):
        """
        Implements the drawing algorithm for the FA
        """
        raise NotImplementedError

    def dump(self, object, filename):
        """
        dumps a serialized version of any object inside the class

        :param object: any class attribute
        :param filename: filename in which the serialized object is saved
        """
        import pickle

        filename = filename if filename.endswith('.pic') else (filename + '.pic')

        with open(filename, 'wb') as f:
            pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)

    def dump_json(self, object, filename):
        """
        dumps a json representation of any object inside the class

        :param object: any class attribute
        :param filename: filename in which the json object is saved
        """
        import json

        filename = filename if filename.endswith('.json') else (filename + '.json')

        with open(filename, 'w') as f:
            json.dump(object, f, indent=4)
