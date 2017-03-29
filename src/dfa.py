from networkx import *
import matplotlib.pyplot as plt


class DFA:
    def __init__(self, nfa):
        self.start_node = None
        self.end_node = None
        self.graph = DiGraph()

        self.generate_dfa(nfa)

    def generate_dfa(self, nfa):
        self.start_node = nfa.start_node

        start_state = nfa.epsilon_closure(nfa.start_node)
