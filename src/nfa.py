from networkx import *
import matplotlib.pyplot as plt

from src.helpers import *


class NFA:
    # current node index is kept as a static variable to ensure that
    # no two node are given the same index
    __cni = 1

    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.graph = Graph()

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

    def get_node_index(self):
        self.__cni += 1
        return self.__cni - 1

    def from_simple_regex(self, regex):
        """"
        This method create an NFA from a simple regex without union,
         concatenation or kleene closure operations
        """
        # TODO : Add Doctests

        last_char = None
        for i in range(len(regex)):
            char = regex[i]
            if is_letter(char):
                last_char = char
                # check if this char is not the start or the end of a range
                if (i == len(regex) - 1 and regex[i - 1] != '-') or (i + 1 < len(regex) and regex[i + 1] != '-'):
                    self.concatenate_node(char)
            elif char == '-' and last_char is not None:
                start_char = last_char
                end_char = regex[i + 1 if i + 1 < len(regex) else None]
                if end_char:
                    self.add_nodes_in_range(start_char, end_char)
                else:
                    raise ValueError("""
                                    "a-" is not a valid Regex format.
                                     End range must be specified
                                     """)
            else:
                raise ValueError('Error in Regex format')

    def concatenate_node(self, edge_weight):
        self.graph.add_node(self.get_node_index())
        self.graph.add_weighted_edges_from([(self.__cni - 2, self.__cni - 1, ord(edge_weight))])

    def add_nodes_in_range(self, start_char, end_char):
        # create start and end nodes
        self.start_node = self.get_node_index()
        self.end_node = self.get_node_index()
        for char_ord in range(ord(start_char), ord(end_char) + 1):
            # connect starting node to first node before character
            self.graph.add_weighted_edges_from([(self.start_node, self.get_node_index(), 0)])
            # connect first node before character to the node after character
            self.graph.add_weighted_edges_from([(self.__cni - 1, self.get_node_index(), char_ord)])
            # connect node after character with end node
            self.graph.add_weighted_edges_from([(self.__cni - 1, self.end_node, 0)])

    def concatenate(self, nfa):
        # TODO : test
        # connect the end of the first graph with the start of the second
        self.graph.add_weighted_edges_from(self.end_node, nfa.start_node, 0)
        # add the second graph edges to self.graph
        self.graph = nx.compose(self.graph, nfa.graph)

    def union(self, nfa):
        # TODO : test
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
        pos = shell_layout(self.graph, scale=2)
        draw_networkx(self.graph, pos)
        draw_networkx_edge_labels(self.graph, pos=pos, edge_labels=el)
        plt.show()
