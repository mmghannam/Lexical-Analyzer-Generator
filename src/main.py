from src.dfa import *
from src.nfa import *
from src.tokenizer import *
from src.grammar import Grammar

g = Grammar()
nfa = NFA.from_tokens(g.get_token_list())
print('start: ', nfa.start_node)
print('end: ', nfa.end_node)

# print(nfa.move(1, {1, 2}))

dfa = DFA(nfa, 'test.txt')

# nfa.draw()

# reader = Reader('test.txt')
# print(reader.getTokens())
