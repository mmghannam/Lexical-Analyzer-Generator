from src.dfa import *
from src.nfa import *
from src.grammar import Grammar
from src.grammar_token import GrammarToken

tokens = [
    GrammarToken('bibo', '(0|1)*0(0|1)')
]
nfa = NFA.from_tokens(tokens)

g = Grammar(path='./grammar.txt')
# nfa = NFA.from_grammar(g)

print('start: ', nfa.start_node)
print('end: ', nfa.end_node)

dfa = DFA(nfa, 'test.txt')
# nfa.draw()
