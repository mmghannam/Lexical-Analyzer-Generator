import doctest

import matplotlib.pyplot as plt
import networkx as nx

from src.nfa import *

# loading doctests
doctest.testmod()

nfa = NFA()

nfa.from_simple_regex('a-c')

nfa.draw()
