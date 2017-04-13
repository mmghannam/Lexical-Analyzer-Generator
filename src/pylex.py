from src.dfa import DFA
from src.grammar import Grammar
from src.nfa import NFA


class Pylex:
    def __init__(self):
        self.grammar = None
        self.nfa = None
        self.dfa = None

    def read_grammar(self, path):
        self.grammar = Grammar(path)

    def generate_nfa(self):
        # tokens = [
        #     GrammarToken('test', '(0|1)*0')
        # ]
        # self.nfa = NFA.from_tokens(tokens)

        self.nfa = NFA.from_grammar(self.grammar)

        print('start: ', self.nfa.start_node, ', end: ', self.nfa.end_node)

        # self.nfa.draw()

    def generate_dfa(self):
        if self.nfa:
            self.dfa = DFA(self.nfa)
        else:
            raise ValueError('NFA was not generated.')

    def read_source_code(self, path):
        if self.dfa:
            self.dfa.read_token_stream(path)
        else:
            raise ValueError('DFA was not generated.')
