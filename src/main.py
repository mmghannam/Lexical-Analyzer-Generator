from src.nfa import *
from src.tokenizer import *
tokens = [Token('ab(a|b)*', 'bibo')]
nfa = NFA.from_tokens(tokens)
print('start: ', nfa.start_node)
print('end: ', nfa.end_node)
nfa.draw()
