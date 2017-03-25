import doctest

import matplotlib.pyplot as plt
import networkx as nx

from src.nfa import *

# loading doctests
doctest.testmod()

nfa = NFA()
nfa2 = NFA()
nfa.from_simple_regex('a-z')
nfa2.from_simple_regex('b')
nfa.union(nfa2)
nfa.draw()
