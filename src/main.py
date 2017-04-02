from src.dfa import *
from src.nfa import *
from src.grammar_token import GrammarToken

tokens = [
    GrammarToken('bibo', '(0|1)*0(0|1)')
    # GrammarToken(',', ','),
    # GrammarToken('\\(', '\\)'),
    # GrammarToken('a-z(a-z|0-9)*', 'id'),
    # GrammarToken('if', 'if'),
    # GrammarToken('\\*|\\/', 'mulop')
]

nfa = NFA.from_tokens(tokens)

print('start: ', nfa.start_node)
print('end: ', nfa.end_node)

# dfa = DFA(nfa, 'test.txt')
nfa.draw()
