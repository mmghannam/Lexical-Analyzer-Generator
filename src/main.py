from src.dfa import *
from src.grammar import Grammar
from src.nfa import *

g = Grammar()
nfa = NFA.from_tokens(g.get_token_list())
print('start: ', nfa.start_node)
print('end: ', nfa.end_node)

dfa = DFA(nfa, 'test.txt')

# nfa.draw()
