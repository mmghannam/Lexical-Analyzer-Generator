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

        self.nfa.draw()

    def generate_dfa(self):
        self.dfa = DFA(self.nfa)

    def read_source_code(self, path):
        self.dfa.read_token_stream(path)
