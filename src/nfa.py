from networkx import *
import matplotlib.pyplot as plt

from src.helpers import *


class NFA:
    # current node index is kept as a static variable to ensure that
    # no two node are given the same index
    cni = 1

    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.graph = DiGraph()

    def parse_tokens(self, tokens):
        """
        This method implements a shunting-yard-like algorithm to parse each token's regex
        """
        priority = string_to_priority_hash('()*|+')
        variables_stack = Stack()
        operators_stack = Stack()
        for token in tokens:
            # used character list instead of string to avoid rebuilding the string
            char_group = []
            for char in token.regex:
                if is_letter(char) or char in '-':
                    char_group.append(char)
                elif char in priority:
                    variables_stack.push(''.join(char_group))
                    char_group = []
                    if operators_stack.empty() or priority[char] >= priority[operators_stack.peek()]:
                        operators_stack.push(char)
                    else:
                        pass

    @staticmethod
    def get_node_index():
        NFA.cni += 1
        return NFA.cni - 1

    @staticmethod
    def from_regex(regex):
        import re
        simple_regex = re.compile(r'(.-.|.)+?')
        matches = simple_regex.findall(regex)
        nfa = NFA()
        if len(matches) > 0:
            nfa.from_simple_regex(matches[0])
            for match in matches[1:]:
                nfa.concatenate(NFA().from_simple_regex(match))
            return nfa
        else:
            return None

    def from_simple_regex(self, regex):
        """"
        This method create an NFA from a simple regex without union,
         concatenation or kleene closure operations
         examples : 'a' , 'a-c'
        """
        # TODO : Add Doctests
        if '-' in regex:
            start_char, _, end_char = regex
            if start_char < end_char:
                self.add_nodes_in_range(start_char, end_char)
            else:
                raise ValueError('Error in Regex format, range start must be less than range end.')
        else:
            self.concatenate_node(regex)
        if not self.end_node:
            self.end_node = NFA.cni - 1
        return self

    def concatenate_node(self, edge_weight):
        if not self.start_node:
            self.start_node = self.get_node_index()
        self.graph.add_weighted_edges_from([(NFA.cni - 1, self.get_node_index(), ord(edge_weight))])

    def add_nodes_in_range(self, start_char, end_char):
        # create start node
        self.start_node = self.get_node_index()
        # create end_node
        self.end_node = self.get_node_index()

        for char_ord in range(ord(start_char), ord(end_char) + 1):
            # connect starting node to first node before character
            self.graph.add_weighted_edges_from([(self.start_node, self.get_node_index(), 0)])
            # connect first node before character to the node after character
            self.graph.add_weighted_edges_from([(NFA.cni - 1, self.get_node_index(), char_ord)])
            # connect node after character with end node
            self.graph.add_weighted_edges_from([(NFA.cni - 1, self.end_node, 0)])

    def concatenate(self, nfa):
        # connect the end of the first graph with the start of the second
        self.graph.add_weighted_edges_from([(self.end_node, nfa.start_node, 0)])
        # add the second graph edges to self.graph
        self.graph = nx.compose(self.graph, nfa.graph)
        # update new end node with the second nfa's end node
        self.end_node = nfa.end_node

    def union(self, nfa):
        last_start_node = self.start_node
        last_end_node = self.end_node
        self.start_node = self.get_node_index()
        self.end_node = self.get_node_index()

        # connect new start to both starts of the two graphs
        self.graph.add_weighted_edges_from([(self.start_node, last_start_node, 0)])
        self.graph.add_weighted_edges_from([(self.start_node, nfa.start_node, 0)])

        # connect the two ends of the graphs with the new end
        self.graph.add_weighted_edges_from([(last_end_node, self.end_node, 0)])
        self.graph.add_weighted_edges_from([(nfa.end_node, self.end_node, 0)])

        # add the second graph edges to self.graph
        self.graph = nx.compose(self.graph, nfa.graph)

    def draw(self):
        el = get_edge_attributes(self.graph, 'weight')
        pos = circular_layout(self.graph, scale=2)
        draw_networkx(self.graph, pos)
        draw_networkx_edge_labels(self.graph, pos=pos, edge_labels=el)
        plt.show()

    def merge_nodes(self, nodes, new_node):
        """
        Merges selected `nodes` of self.graph into a new_node
        """

        self.graph.add_node(new_node)  # Add the 'merged' node

        for n1, n2, data in self.graph.edges(data=True):
            # For all edges related to one of the nodes to merge,
            # make an edge going to or coming from the `new gene`.
            if n1 in nodes:
                self.graph.add_edge(new_node, n2, data)
            elif n2 in nodes:
                self.graph.add_edge(n1, new_node, data)

        for n in nodes:  # remove the merged nodes
            self.graph.remove_node(n)
