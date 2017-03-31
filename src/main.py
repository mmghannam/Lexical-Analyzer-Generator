from src.dfa import *
from src.nfa import *
from src.tokenizer import *

nfa = NFA.from_tokens([Token('(0|1)*0(0|1)', 'bibo')])
print('start: ', nfa.start_node)
print('end: ', nfa.end_node)

# print(nfa.move(1, {1, 2}))

dfa = DFA(nfa, 'test.txt')

# nfa.draw()

# reader = Reader('test.txt')
# print(reader.getTokens())
