# import unittest
import pprint as pp
import re
from enum import Enum
from src.tokenizer import Token

import src.regex_expander as regexex


class TokenType(Enum):
    letter = 0
    digit = 1
    identifier = 2  # if else while
    digits = 3
    type = 4  # boolean int float
    num = 5
    rel_op = 6
    assignment_op = 7
    reserved_word = 8
    punctuation = 9
    add_op = 10
    mul_op = 11
    labmda = 12


class Grammar:
    non_terminals = {
        'id': 'letter(letter | digit) *',
        'num': 'digit+ | digit+ . digits ( \L | E digits)',
        'relop': "\=\= | !\= | > | >\= | < | <\=".replace(' ', ''),
        'addop': '\+ | -'.replace(' ', ''),
        'mulop': '\* | /'.replace(' ', ''),
        'assign': '=',
        'digits': 'digit+'
    }

    terminals = {
        'letter': 'a-z',
        'digit': '0-9',
        'L': '@',
        'E': 'exp',
    }

    def __init__(self, path=None):
        self.classes = []

        self.letters = regexex.generate_range('a', 'z')
        self.numbers = regexex.generate_range('0', '9')

        self.classes.append((TokenType.letter, self.letters))
        self.classes.append((TokenType.digit, self.numbers))
        self.classes.append((TokenType.reserved_word, ['if', 'else', 'while']))
        self.classes.append((TokenType.type, ['boolean', 'int', 'float']))
        self.classes.append((TokenType.rel_op, ['==', '!=', '>', '>=', '<', '<=']))
        self.classes.append((TokenType.assignment_op, ['=']))
        self.classes.append((TokenType.add_op, ['+', '-']))

        # for file parsing, check if a line starts with [,{
        keywords = '{if else while}'
        types = '{boolean int float}'

        punct = '[; , \( \) { }]'
        self.add_as_reserved(punct, self.non_terminals)

        self.add_as_reserved(keywords, self.non_terminals)
        self.add_as_reserved(types, self.non_terminals)

        self.flatten_dict_definitions()

    def flatten_dict_definitions(self):

        for prod_k, prod_v in self.non_terminals.items():

            # Replace terminals in other terminals, TODO recursively parse it
            for terminal, sequence in self.terminals.items():
                self.non_terminals[prod_k] = prod_v = re.sub('(' + terminal + '(?!\w))', sequence, prod_v)

            # Replace non terminals
            for non_term, seq in self.non_terminals.items():
                self.non_terminals[prod_k] = prod_v = re.sub('(' + non_term + '(?!\w))', seq, prod_v)

    def add_as_reserved(self, char_def, grammar_dict):
        # Expand definitions to key-value pairs
        expanded_def = self.ultimate_expander(char_def)
        # Add updates to the main dictionary
        self.__expand_dictionary(grammar_dict, expanded_def)

    @staticmethod
    def __expand_dictionary(dictionary, key_value_list):
        [dictionary.update(kv) for kv in key_value_list]

    @staticmethod
    def ultimate_expander(rule: str):
        """
        Cleans up a line which contains a definition, then maps each item to itself
        :param rule: rule definition e.x '{if else}' -> {'if':'if'} , {'else':'else'}
        :return: list of key:value pairs
        """
        rule = rule.strip()
        tokens = rule.replace(rule[0], '').replace(rule[-1], '')

        token_list = tokens.split(' ')

        return [{t: t.replace('\\', '')} for t in token_list]

    def get_token_list(self):
        tokens = []
        for k, v in g.non_terminals.items():
            tokens.append(Token(v.replace(' ', ''), k))
        return tokens

"""
Tests
"""

# class TestStringMethods(unittest.TestCase):
#     pass


# def test_open_file(self):
#     tests_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test-files'))
#     grammar = Grammar(tests_path + '/test_grammar.txt')
#     self.assertEqual(grammar.pre_process(), 1)
#     print("file:", __file__)
#
# def test_expand_pattern(self):
#     gra = Grammar()
#     gra.expand_pattern('ch=a-b')
#     self.assertEqual(set(gra.expand_pattern('x = a-b|1-3')[1]), {'a', 'b', '1', '2', '3'})


if __name__ == '__main__':
    # unittest.main()
    g = Grammar()
    pp.pprint(g.non_terminals)