from src.nfa import *
from src.dfa import *
from src.tokenizer import *

nfa = NFA.from_tokens([Token('a(a|b)*', 'bibo')])
print('start: ', nfa.start_node)
print('end: ', nfa.end_node)

# print(nfa.move(1, {1, 2}))

# dfa = DFA(nfa)

nfa.draw()
