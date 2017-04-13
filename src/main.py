from src.pylex import Pylex

pylex = Pylex()

pylex.read_grammar(path='./grammar.txt')
pylex.generate_nfa()
pylex.generate_dfa()
pylex.read_source_code(path='test.txt')
