import doctest

import matplotlib.pyplot as plt
import networkx as nx

from src.nfa import *

# loading doctests
doctest.testmod()

nfa = NFA()

nfa.from_simple_regex('a-c')

for x, y in nfa:
    print(x, y)
    print('=' * 100)

nfa.draw()
