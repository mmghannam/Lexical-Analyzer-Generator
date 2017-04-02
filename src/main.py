from src.dfa import *
from src.grammar import Grammar
from src.nfa import *
from src.tokenizer import Token

tokens = [
    Token(',', ','),
    Token('\\(', '\\)'),
    # Token('a-z(a-z|0-9)*', 'id'),
    Token('if', 'if'),
    Token('\\*|\\/', 'mulop')
]
nfa = NFA.from_tokens(tokens)
print('start: ', nfa.start_node)
print('end: ', nfa.end_node)

# dfa = DFA(nfa, 'test.txt')
nfa.draw()
