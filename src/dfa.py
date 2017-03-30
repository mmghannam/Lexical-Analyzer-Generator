from networkx import *
from .dfa_state import *
import matplotlib.pyplot as plt


class DFA:
    def __init__(self, nfa):
        self.start_node = None
        self.end_node = None
        self.graph = DiGraph()

        self.generate_dfa(nfa)

    def generate_dfa(self, nfa):
        self.start_node = nfa.start_node

        states = set()

        start_state = DFAState(nfa.get_epsilon_closures(nfa.start_node))
        states.add(start_state)

        print(start_state)

    def is_letter(self, char):
        return (ord('a') <= ord(char) <= ord('z')) or \
               (ord('A') <= ord(char) <= ord('Z'))

    def is_digit(self, num):
        return (ord('0') <= ord(num) <= ord('9')) if isinstance(num, str) \
            else (0 <= num <= 9)
