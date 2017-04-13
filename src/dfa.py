import string
from collections import namedtuple, OrderedDict

import matplotlib.pyplot as plt
from networkx import *
from prettytable import PrettyTable

from src.fa import *
from src.nfa import *
from .reader import Reader

DFAState = namedtuple('DFAState', ['index', 'NFAStates', 'acceptance', 'token'])


class DFA(FA):
    def __init__(self, nfa):
        super().__init__()
        self.transition_table = {}
        self.init_input_list()

        self.rejection_state = None
        dfa = self.generate_dfa(nfa, minimize=False)
        self.__copy__(dfa)

        # after DFA stuff
        self.accepted_tokens = []
        self.symbol_table = {}

    # DFA graph
    def generate_dfa(self, nfa, minimize=False):
        """
        Applies the Subset Construction Algorithm to generate a DFA
            for a corresponding NFA

        If minimize is set to True, then the minimization algorithm
            will be used to reduced the resulting DFA
        """
        new_dfa = FA()

        start_state = DFAState(new_dfa.get_node_index(), nfa.get_epsilon_closures(nfa.start_node), False, None)
        new_dfa.increment_node_index()

        worklist = list()
        new_dfa.states.append(start_state)
        worklist.append(start_state)

        while worklist:
            current_state = worklist.pop()

            for input_literal in self.input_list:
                # get new state by moving under input
                new_nfa_states = nfa.get_epsilon_closures(nfa.move(current_state.NFAStates, input_literal))

                is_acceptance, token = nfa.check_acceptance(new_nfa_states)
                new_dfa_state = DFAState(new_dfa.get_node_index(), new_nfa_states, is_acceptance, token)
                # check if state already exists
                state_exists, index = new_dfa.state_exists(new_dfa_state)

                if not state_exists:  # new state
                    new_dfa.states.append(new_dfa_state)
                    worklist.append(new_dfa_state)

                    if not new_nfa_states:
                        self.rejection_state = new_dfa_state

                    new_dfa.graph.add_weighted_edges_from([(current_state.index, index, input_literal)])
                    new_dfa.increment_node_index()
                else:  # already exists, don't add to worklist
                    new_dfa.graph.add_weighted_edges_from([(current_state.index, index, input_literal)])

        # self.draw(new_dfa.graph)

        if minimize:
            new_dfa = self.minimize(new_dfa)

        self.generate_transition_table(new_dfa)

        return new_dfa

    # Minimization Functions
    def minimize(self, fa):
        """
        Applies Brzozowski's minimization Algorithm
        """
        R1 = self.reverse(fa)
        R1.start_node = self.get_start_node(R1.graph)
        # self.draw(R1.graph)

        D1 = self.generate_dfa(R1)
        # self.draw(D1.graph)

        R2 = self.reverse(D1)
        R2.start_node = self.get_start_node(R2.graph)
        # self.draw(R2.graph)

        D2 = self.generate_dfa(R2)
        # self.draw(D2.graph)

        return D2

    def reverse(self, fa, copy=True):
        """Return the reverse of the graph.

        The reverse is a graph with the same nodes and edges
        but with the directions of the edges reversed.

        Doesn't change the original graph
        """
        graph = self.add_last_node(fa, copy)
        # graph = fa.graph.copy() if copy else fa.graph

        if copy:
            from copy import deepcopy

            R = graph.__class__(name="Reverse of (%s)" % graph.name)
            R.add_nodes_from(graph.nodes())
            R.add_edges_from((v, u, k, deepcopy(d)) for u, v, k, d
                             in graph.edges(keys=True, data=True))
            R.graph = deepcopy(graph.graph)
            R.node = deepcopy(graph.node)
            new_fa = NFA()
            new_fa.__copy__(fa)
            new_fa.graph = R
            return new_fa

        else:
            graph.pred, graph.succ = graph.succ, graph.pred
            graph.adj = graph.succ
            R = graph
            fa.graph = R
            return fa

    def add_last_node(self, fa, copy=True):
        """
        Adds a node after all accepting nodes, to help in
            reversing algorithm
        """
        graph = fa.graph.copy() if copy else fa.graph

        last = DFAState(fa.get_node_index(), {}, True, None)

        for node in graph.copy().nodes_iter():
            if fa.states[node].acceptance:
                fa.states[node] = DFAState(fa.states[node].index, fa.states[node].NFAStates, False,
                                           fa.states[node].token)
                graph.add_weighted_edges_from([(node, last.index, DFA.epsilon)])

        return graph

    def get_start_node(self, graph):
        """
        Use BFS to find the starting node of an NFA
        """
        all_keys, all_values = set(), set()

        for x in graph.nodes():
            l = bfs_predecessors(graph, x)
            all_keys.update(l.keys())
            all_values.update(l.values())

        return int(list(all_values - all_keys)[0])

    # Transition Table
    def generate_transition_table(self, fa=None):
        """
        Generates a transition table from a given graph
        """
        G = self.graph if fa is None else fa.graph

        for node in G.nodes_iter():
            self.transition_table[node] = OrderedDict()

            for u, v, d in G.out_edges(node, data=True):
                self.transition_table[node][d['weight']] = v

                # self.print_transition_table(fa)
                # FA.dump(self.transition_table, 'table.pic')
                # FA.dump_json(self.transition_table, 'table.json')

    def load_table(self):
        import pickle

        with open('table.pic', 'rb') as t:
            self.transition_table = pickle.load(t)

    def print_transition_table(self, fa=None):
        states = self.states if fa is None else fa.states
        print('=' * 100)
        table = PrettyTable(['State'] + [x for x in self.input_list])

        for index in self.transition_table:
            row = self.transition_table[index]
            state = str(index) + ': ' + (str(states[index].NFAStates)) \
                if states[index].NFAStates else 'Rejection'
            table.add_row([state] + [row[x] for x in row])

        print(table)

    # Utilities
    def init_input_list(self):
        """
        initiate list with all possible input symbols
        """
        letters = list(string.ascii_letters)
        digits = list(string.digits)
        operators = ['!', '>', '<',  # relational operators ('==', '!=', '>', '>=', '<', '<=')
                     '=',  # assignment operator
                     '+', '-',  # add operators
                     '*', '/',  # multiply operators
                     ';', ',', '(', ')', '{', '}'  # reserved operators
                     ]

        self.input_list = letters + digits + operators
        # self.input_list = '01'

    def draw(self, graph=None):
        G = self.graph if graph is None else graph

        for u, v, d in G.edges(data=True):
            d['label'] = d.get('weight', '')

        g = networkx.drawing.nx_agraph.to_agraph(G)
        g.layout()
        g.draw('DFA.png')

        import matplotlib.image as mpimg

        img = mpimg.imread('DFA.png')
        plt.figure()
        plt.imshow(img)
        plt.show()

    # Source Code File Functions
    def move(self, node_index, input):
        '''
        :param node_index: source node index
        :param input: input literal
        :return: new node index
        '''
        try:
            target = self.transition_table[node_index][input]
        except KeyError:
            target = self.rejection_state.index

        return target

    def read_token_stream(self, filename):
        """
        reads token stream from a file and runs each token
        through the DFA.

        writes tokens to output file

        :param filename: name of file to be read
        """
        tokens = Reader(filename).getTokens()

        for token in tokens:
            if not self.accept_token(token):
                print('Lexical Error in', token)
                token = token[:-1]
                print('--->>> Recovering...')
                while not self.accept_token(token) and token:
                    print('\ttried:', token)
                    token = token[:-1]
                if token:
                    print('accepted as :', token)
                else:
                    print('Recovery failed.')

        f = open('output.txt', 'w')
        for accepted_token in self.accepted_tokens:
            f.write(accepted_token + '\n')

        f.close()

        FA.dump(self.symbol_table, 'symbol_table.pic')
        FA.dump_json(self.symbol_table, 'symbol_table.json')

    def accept_token(self, token):
        """
        Runs a token through the DFA
        If it passes, it is added to the list

        :param token: a single token to test
        """
        current_state_index = 0  # start node
        for char in token:
            current_state_index = self.move(current_state_index, char)

        current_state = self.states[current_state_index]
        if current_state.acceptance:
            self.accepted_tokens.append(current_state.token)

            if current_state.token == 'id':
                self.symbol_table[token] = {}
            return True
        else:
            return False



