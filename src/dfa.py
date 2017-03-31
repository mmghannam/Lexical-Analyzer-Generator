from collections import namedtuple, OrderedDict
from networkx import *
import matplotlib.pyplot as plt
import string
from prettytable import PrettyTable

DFAState = namedtuple('DFAState', ['index', 'NFAStates', 'acceptance'])


class DFA:
    def __init__(self, nfa):
        self.start_node = None
        self.end_node = None
        self.node_index = 0
        self.transition_table = {}

        self.init_input_list()
        self.generate_dfa(nfa)

    def generate_dfa(self, nfa):
        self.start_node = nfa.start_node

        self.states = list()
        worklist = list()

        start_state = DFAState(self.get_node_index(), nfa.get_epsilon_closures(nfa.start_node), False)
        # print(start_state)

        self.states.append(start_state)
        worklist.append(start_state)

        # worklist is a list that contains any new DFA state generated
        while worklist:
            current_state = worklist.pop()
            self.transition_table[current_state.index] = OrderedDict()

            # for every input
            for input_literal in self.input_list:
                # get new state by moving under input
                new_nfa_states = nfa.get_epsilon_closures(nfa.move(current_state.NFAStates, input_literal))

                # not going anywhere
                if not new_nfa_states:  # rejection
                    self.transition_table[current_state.index][input_literal] = None
                    continue

                is_acceptance = nfa.check_acceptance(new_nfa_states)
                new_dfa_state = DFAState(self.get_node_index(), new_nfa_states, is_acceptance)

                # check if state already exists
                state_exists, index = self.state_exists(new_dfa_state)

                if not state_exists:  # new state
                    self.states.append(new_dfa_state)
                    worklist.append(new_dfa_state)

                    self.transition_table[current_state.index][input_literal] = index
                    self.increment_node_index()
                else: # already exists, don't add to worklist
                    self.transition_table[current_state.index][input_literal] = index

        self.print_transition_table()

    def state_exists(self, new_state):
        for state in self.states:
            if new_state.NFAStates == state.NFAStates:
                return True, state.index

        return False, new_state.index

    def is_letter(self, char):
        return (ord('a') <= ord(char) <= ord('z')) or \
               (ord('A') <= ord(char) <= ord('Z'))

    def is_digit(self, num):
        return (ord('0') <= ord(num) <= ord('9')) if isinstance(num, str) \
            else (0 <= num <= 9)

    def get_node_index(self):
        return self.node_index

    def increment_node_index(self):
        self.node_index += 1

    def print_transition_table(self):

        print('=' * 100)

        table = PrettyTable(['State'] + [x for x in self.input_list])

        for index in self.transition_table:
            row = self.transition_table[index]

            state = str(index) + ': ' + (str(self.states[index].NFAStates)) \
                if self.states[index].NFAStates else 'Rejection'

            table.add_row([state] + [row[x] for x in row])

        print(table)

    def init_input_list(self):
        letters = list(string.ascii_letters)
        digits = list(string.digits)
        operators = [  # '==', '!=', '>', '>=', '<', '<=',  # relational operators
            '=',  # assignment operator
            '+', '-',  # add operators
            '*', '/',  # multiply operators
            ';', ',', '(', ')', '{', '}'  # reserved operators
        ]

        # self.input_list = letters + digits + operators
        self.input_list = '01'
