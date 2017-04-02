# import unittest
import re
from src.grammar_token import GrammarToken


class Grammar:
    def __init__(self, path=None):

        # for file parsing, check if a line starts with [,{

        self.path = path
        self.__terminals = []
        self.__non_terminals = []

        # Add the epsilon
        self.__terminals.append(GrammarToken("lambda", "\L"))
        # self.terminals.append(Token("E", "exp"))

    def parse_file(self):
        lines = open(self.path).readlines()
        for line in lines:

            if line.startswith('{'):
                self.create_reserved_word_token(line)

            elif line.startswith('['):
                self.create_reserved_word_token(line)

            else:
                self.parse_rule(line)

        self.expand_non_terminals()

    def get_terminals(self):
        return self.__terminals

    def get_non_terminals(self):
        return self.__non_terminals

    def parse_rule(self, line: str):
        """
        Takes a rule line and adds it to the terminals / non-terminals as appropriate
        :param line: input file line
        """
        splits = [item.strip() for tup in re.findall(r'(.+)(?<=\w|\s)(=|:)(?=\w|\s)(.+)', line.strip()) for item in tup]

        # If any number other than 3 groups are matched, raise an error
        if len(splits) != 3:
            raise RuntimeError("Malformed rule ", line)

        rule_name = splits[0]
        rule_assigner = splits[1]

        tok = GrammarToken(rule_name, splits[2].replace(' ', ''))

        if rule_assigner == '=':
            self.__terminals.append(tok)
        elif rule_assigner == ':':
            self.__non_terminals.append(tok)
        else:
            raise RuntimeError("Undefined rule type")

    def create_reserved_word_token(self, line):
        """
        Creates a token object for reserved words and punctuations
        example: { int float double }
        :param line: name of the new token
        :param line: 
        :return: 
        """
        filtered = line[1:-2]  # Remove the brackets/braces surrounding the rule
        keywords = filter(None, filtered.split(' '))

        for word in keywords:
            word = word.replace(' ', '')
            self.__non_terminals.append(GrammarToken(word, word))

    def expand_non_terminals(self):
        """
        Takes the raw grammar rules and expands the non-terminals then
         the terminals inside this rule
        """
        for non_terminal in self.__non_terminals:
            partially_flattened = self.flatten_non_terminals(non_terminal.regex)
            non_terminal.regex = self.flatten_terminals(partially_flattened)

    def flatten_non_terminals(self, input_rule: str):
        """
        Expands all non terminals in a given rule 
        i.e ( note the assignment operator : , = )
        terminal_x = 5-7
        non_term_b : a-x | 3-4 | terminal_x
        non_term_a : 0-9 | non_term_b
        
        the function output will be 
        non_term_a: 0-9 | a-x | 3-4 | terminal_x
        
        :param input_rule: rule to flatten its non terminals
        :return: a partially flattened grammar rule
        """
        for non_terminal in self.__non_terminals:
            non_terminal_name = non_terminal.name
            if non_terminal_name is not input_rule and non_terminal_name in input_rule:
                non_terminal_regex = '(' + non_terminal_name + '(?!\w))'
                # Solve part of the problem, then recurse
                input_rule = re.sub(non_terminal_regex, non_terminal.regex, input_rule)
                input_rule = self.flatten_non_terminals(input_rule)

        return input_rule

    def flatten_terminals(self, input_rule: str):
        """
        Expands terminals found in a grammar rule after substituting the non terminals
        :param input_rule: rule to expand
        :return: a fully flattened grammar rule
        """
        for terminal in self.__terminals:
            temp = ""

            # No more of this non terminal exists
            # and
            # Don't expand yourself
            while temp is not input_rule \
                    and input_rule is not terminal.regex:

                temp = input_rule
                # Find a terminal name followed by special symbols only
                # case: digit+ digits -> don't match 'digit' that's in 'digits'
                terminal_regex = r'(' + terminal.name + '(?!\w))'

                try:
                    # Solve part of the problem and recurse, DFS like way to replace
                    # all non terminals
                    input_rule = re.sub(terminal_regex, terminal.regex, input_rule)

                    if temp is input_rule:
                        break

                    # If something changed, there might be more stuff to expand
                    input_rule = self.flatten_terminals(input_rule)

                except Exception as err:
                    print(err, 'source:', terminal_regex)
        return input_rule


# Main function
if __name__ == '__main__':
    g = Grammar('../test-files/test_grammar.txt')
    g.parse_file()

    print("Terminals:")
    for thing in g.get_terminals():
        print(thing)

    print("Tokens:")
    for token in g.get_non_terminals():
        print(token)
