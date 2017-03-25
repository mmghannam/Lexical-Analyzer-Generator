import doctest

import matplotlib.pyplot as plt
import networkx as nx

from src.nfa import *

# loading doctests
doctest.testmod()

nfa = NFA.from_regex('a-bc-d')
nfa.draw()
