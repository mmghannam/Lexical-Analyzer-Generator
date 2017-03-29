from src.nfa import *
from src.tokenizer import *

nfa = NFA.from_tokens([Token('bac', 'bibo')])
print('start: ', nfa.start_node)
print('end: ', nfa.end_node)
nfa.draw()
