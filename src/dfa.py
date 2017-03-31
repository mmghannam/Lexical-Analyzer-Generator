import string
from collections import namedtuple, OrderedDict

from prettytable import PrettyTable

from .reader import Reader

DFAState = namedtuple('DFAState', ['index', 'NFAStates', 'acceptance', 'token'])


class DFA:
    def __init__(self, nfa, filename):
        self.start_node = None
        self.end_node = None
        self.node_index = 0
        self.transition_table = {}

        self.init_input_list()
        self.generate_dfa(nfa)

        # after DFA stuff
        self.accepted_tokens = []
        self.read_token_stream(filename)

    def generate_dfa(self, nfa):
        self.states, worklist = list(), list()

        start_state = DFAState(self.get_node_index(), nfa.get_epsilon_closures(nfa.start_node), False, None)
        self.increment_node_index()

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

                is_acceptance, token = nfa.check_acceptance(new_nfa_states)
                new_dfa_state = DFAState(self.get_node_index(), new_nfa_states, is_acceptance, token)
                # check if state already exists
                state_exists, index = self.state_exists(new_dfa_state)

                if not state_exists:  # new state
                    self.states.append(new_dfa_state)
                    worklist.append(new_dfa_state)

                    self.transition_table[current_state.index][input_literal] = index
                    self.increment_node_index()
                else:  # already exists, don't add to worklist
                    self.transition_table[current_state.index][input_literal] = index

        self.print_transition_table()

    def state_exists(self, new_state):
        for state in self.states:
            if new_state.NFAStates == state.NFAStates:
                return True, state.index

        return False, new_state.index

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

        self.input_list = letters + digits + operators
        # self.input_list = '01'

    def move(self, node_index, input):
        return self.transition_table[node_index][input]

    def read_token_stream(self, filename):
        tokens = Reader(filename).getTokens()

        for token in tokens:
            self.accept_token(token)

        f = open('output.txt', 'w')
        for accepted_token in self.accepted_tokens:
            f.write(accepted_token + ',\n')

        f.close()

    def accept_token(self, token):
        current_state_index = 0  # start node
        for char in token:
            current_state_index = self.move(current_state_index, char)

        current_state = self.states[current_state_index]
        if current_state.acceptance:
            self.accepted_tokens.append(current_state.token)
