from src.dfa import *
from src.grammar import Grammar
from src.nfa import *

g = Grammar(path='src/grammar.txt')
nfa = NFA.from_grammar(g)
print('start: ', nfa.start_node)
print('end: ', nfa.end_node)

# dfa = DFA(nfa, 'test.txt')
nfa.draw()
