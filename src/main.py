from src.dfa import *
from src.grammar import Grammar
from src.grammar_token import GrammarToken
from src.nfa import *

tokens = [
    GrammarToken('bibo', '(0|1)*0(0|1)')
]
nfa = NFA.from_tokens(tokens)

# g = Grammar(path='./grammar.txt')
# nfa = NFA.from_grammar(g)

print('start: ', nfa.start_node)
print('end: ', nfa.end_node)

nfa.draw()

# dfa = DFA(nfa)
# dfa.generate_dfa(nfa)
# dfa.read_token_stream('test.txt')
