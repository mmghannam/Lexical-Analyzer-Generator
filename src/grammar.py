import pathlib
import unittest
import os


class Grammar:
    def __init__(self, path):
        self.tokens = []
        self.__file_contents = pathlib.Path(path).read_text().split('\n')

    def pre_process(self):
        # TODO:
        # open file
        # initialize tokens list
        # add each token to list in the form of a tuple ( REGEX, token_name )
        # return Grammar(tokens)
        for line in self.__file_contents:
            (prod_name, pattern) = self.expand_pattern(line)

        return 1

    def expand_pattern(self, line):
        words = line.split(' ')

        if len(words) < 3:
            raise RuntimeError('Line doesnt have enough arguments')

        assignment_op = words[1]

        if assignment_op == '=':
            pass  # TODO define new char class

        if assignment_op == ':':
            pass  # TODO expand a regex

        self.tokens.append([]);


"""
Tests
"""


class TestStringMethods(unittest.TestCase):
    def test_open_file(self):
        tests_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test-files'))
        grammar = Grammar(tests_path + '/test_grammar.txt')
        self.assertEqual(grammar.pre_process(), 1)
        print("file:", __file__)


if __name__ == '__main__':
    unittest.main()
