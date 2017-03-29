from networkx import *
import matplotlib.pyplot as plt

from src.helpers import *


class NFA:
    # current node index is kept as a static variable to ensure that
    # no two node are given the same index
    __cni = 1

    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.graph = DiGraph()

    @staticmethod
    def from_tokens(tokens):
        if len(tokens) > 0:
            first_token_nfa = NFA.from_regex(add_concatenation_operator_to_regex(tokens[0].regex))
            first_token_nfa.graph.node[first_token_nfa.end_node]['acceptance'] = tokens[0].name
            nfa = first_token_nfa
            for token in tokens[1:]:
                token_nfa = NFA.from_regex(add_concatenation_operator_to_regex(token.regex))
                token_nfa.graph.node[token_nfa.end_node]['acceptance'] = token.name
                # add concatenation operator in regex for easier parsing
                nfa.union(token_nfa)
            return nfa
        else:
            raise ValueError('Tokens list can\'t be empty')

    @staticmethod
    def from_regex(regex, kleene_closure=False):
        """
        This method implements a shunting-yard-like algorithm to parse each token's regex
        """
        priority = string_to_priority_hash('*&|')
        operands = Stack()
        operators = Stack()
        result_nfa = None
        i = 0
        while i < len(regex):
            # keep track of the current char
            current_char = regex[i]
            # checks if its the start of a new expression
            if current_char == '(':
                current_i = i
                # loops till the end of the expression
                while regex[i] != ')':
                    i += 1
                # avoiding out of range error
                if i + 1 < len(regex):
                    # checking for kleene closure expression
                    if regex[i + 1] == '*':
                        result_nfa = NFA.from_regex(regex[current_i + 1:i],
                                                    kleene_closure=True)
                        i += 1
                    else:
                        result_nfa = NFA.from_regex(regex[current_i + 1:i],
                                                    kleene_closure=False)
                # in case the regex ends in ')'
                else:
                    result_nfa = NFA.from_regex(regex[current_i + 1:i],
                                                kleene_closure=False)
            # bypass the end of expression character
            elif current_char == ')':
                pass
            # in case of an escaped special character like '\*'
            elif i < len(regex) - 1 and current_char == '\\':
                operands.push(regex[i + 1])
                # skip the next char
                i += 1
            # checks for operands
            elif current_char not in '*&|':
                # checks for existence of a range in form 'a-c' which is equivalent to 'a|b|c'
                if i < len(regex) - 2 and regex[i + 1] == '-' and regex[i + 2]:
                    operands.push(regex[i:i + 3])
                    i += 3
                    continue
                # in case of a normal operand, examples: 'a','t'
                else:
                    operands.push(current_char)
            # if there are any operators
            elif not operators.empty():
                # only higher priority operators can be pushed to stack ( from shunting-yard algorithm)
                if priority[current_char] >= priority[operators.peek()]:
                    operators.push(current_char)
                else:
                    # perform all operations in stack to be able to push the lower priority operator
                    operator = operators.pop()
                    while operator and priority[current_char] < priority[operator]:
                        if operator == '&':
                            if result_nfa:
                                # create an nfa of only one operand as the result_nfa represents the second operand
                                operand_nfa = NFA.from_simple_regex(operands.pop())
                                # concatenate result_nfa to operand
                                result_nfa = operand_nfa.concatenate(result_nfa)
                            # if result_nfa hasn't been initialized
                            else:
                                # pop two operands
                                second_operand = operands.pop()
                                first_operand = operands.pop()
                                # create an nfa of their concatenation
                                result_nfa = NFA.from_simple_regex(first_operand + second_operand)
                        elif operator == '|':
                            if result_nfa:
                                # create an nfa of only one operand as the result_nfa represents the second operand
                                result_nfa.union(NFA.from_simple_regex(operands.pop()))
                            else:
                                # pop two operands and create corresponding NFA's
                                second_operand_nfa = NFA.from_simple_regex(operands.pop())
                                first_operand_nfa = NFA.from_simple_regex(operands.pop())
                                # create a union of the two NFA's
                                result_nfa = first_operand_nfa.union(second_operand_nfa)

                        operator = operators.pop()
                    # push the lower priority operator
                    operators.push(current_char)
            # if there are no operators in stack
            else:
                operators.push(current_char)
            i += 1

        # perform the remaining operations
        while not operators.empty():
            operator = operators.pop()
            if operator == '&':
                if result_nfa:
                    operand_nfa = NFA.from_simple_regex(operands.pop())
                    result_nfa = operand_nfa.concatenate(result_nfa)
                else:
                    second_operand = operands.pop()
                    first_operand = operands.pop()
                    result_nfa = NFA.from_simple_regex(first_operand + second_operand)
            elif operator == '|':
                if result_nfa:
                    result_nfa.union(NFA.from_simple_regex(operands.pop()))
                else:
                    second_operand_nfa = NFA.from_simple_regex(operands.pop())
                    first_operand_nfa = NFA.from_simple_regex(operands.pop())
                    result_nfa = first_operand_nfa.union(second_operand_nfa)

        # in case of one-character regex
        if not result_nfa and not operands.empty():
            result_nfa = NFA.from_simple_regex(operands.pop())
        # add kleene_closure
        if kleene_closure:
            result_nfa.kleene_closure()
        return result_nfa

    @staticmethod
    def get_node_index():
        """
        This method keeps track of the index of nodes and returns a different index each time by incrementing the static
        class variable __cni
        """
        NFA.__cni += 1
        return NFA.__cni - 1

    @staticmethod
    def from_simple_regex(regex):
        """
        This method creates an NFA from a simple regex containing either characters or ranges
        examples : 'ab-c' , 'bcd' , 'a-z' , 'cfa-dg'
        """
        import re
        simple_regex = re.compile(r'(.-.|.)+?')
        matches = simple_regex.findall(regex)
        nfa = NFA()
        if len(matches) > 0:
            nfa.from_character_or_range(matches[0])
            for match in matches[1:]:
                nfa.concatenate(NFA().from_character_or_range(match))
            return nfa
        else:
            return None

    def from_character_or_range(self, regex):
        """"
        This method create an NFA from a simple regex without union,
         concatenation or kleene closure operations
         examples : 'a' , 'a-c'
        """
        # TODO : Add Doctests
        if '-' in regex:
            start_char, _, end_char = regex
            if start_char < end_char:
                self.add_nodes_in_range(start_char, end_char)
            else:
                raise ValueError('Error in Regex format, range start must be less than range end.')
        else:
            self.concatenate_node(regex)
        if not self.end_node:
            self.end_node = NFA.__cni - 1
        return self

    def concatenate_node(self, edge_weight):
        if not self.start_node:
            self.start_node = self.get_node_index()
        self.graph.add_weighted_edges_from([(NFA.__cni - 1, self.get_node_index(), ord(edge_weight))])

    def add_nodes_in_range(self, start_char, end_char):
        # create start node
        self.start_node = self.get_node_index()
        # create end_node
        self.end_node = self.get_node_index()

        for char_ord in range(ord(start_char), ord(end_char) + 1):
            # connect starting node to first node before character
            self.graph.add_weighted_edges_from([(self.start_node, self.get_node_index(), 0)])
            # connect first node before character to the node after character
            self.graph.add_weighted_edges_from([(NFA.__cni - 1, self.get_node_index(), char_ord)])
            # connect node after character with end node
            self.graph.add_weighted_edges_from([(NFA.__cni - 1, self.end_node, 0)])

    def concatenate(self, nfa):
        if self.start_node and self.end_node:
            # connect the end of the first graph with the start of the second
            self.graph.add_weighted_edges_from([(self.end_node, nfa.start_node, 0)])
            # add the second graph edges to self.graph
            self.graph = nx.compose(self.graph, nfa.graph)
            # update new end node with the second nfa's end node
            self.end_node = nfa.end_node
        # in case the nfa was not assigned to a regex yet
        else:
            self.graph = nfa.graph

        # return self object to allow assignment from method call
        return self

    def union(self, nfa):
        # save last start and end nodes
        last_start_node = self.start_node
        last_end_node = self.end_node

        # create new start and end nodes
        self.start_node = self.get_node_index()
        self.end_node = self.get_node_index()

        # connect new start to both starts of the two graphs
        self.graph.add_weighted_edges_from([(self.start_node, last_start_node, 0)])
        self.graph.add_weighted_edges_from([(self.start_node, nfa.start_node, 0)])

        # connect the two ends of the graphs with the new end
        self.graph.add_weighted_edges_from([(last_end_node, self.end_node, 0),
                                            (nfa.end_node, self.end_node, 0)
                                            ])

        # add the second graph edges to self.graph
        self.graph = nx.compose(self.graph, nfa.graph)

        # return self object to allow assignment from method call
        return self

    def kleene_closure(self):
        # save last end and start nodes
        last_start_node = self.start_node
        last_end_node = self.end_node

        # epsilon transition from last end node to last start node
        self.graph.add_weighted_edges_from([(last_end_node, last_start_node, 0)])

        # create new start and end nodes
        self.start_node = self.get_node_index()
        self.end_node = self.get_node_index()

        # add epsilon transition from new start node to new end node,
        # and add epsilon transition from new start node to new end node
        self.graph.add_weighted_edges_from([(self.start_node, last_start_node, 0),
                                            (last_end_node, self.end_node, 0),
                                            (self.start_node, self.end_node, 0)])

    def plus(self):
        # TODO : Implement in from_regex method
        # epsilon transition from end node to start node
        self.graph.add_weighted_edges_from([(self.end_node, self.start_node, 0)])

    def is_acceptance_node(self, node_index):
        """
        Returns a boolean of whether the given node is an acceptance node
        of a given token in the formal grammar of the input language.
        """
        try:
            self.graph.node[node_index]['acceptance']
            return True
        except:
            return False

    def get_token_name_from_acceptance_node(self, node_index):
        """
        Returns a the token name of the acceptance state given by the node_index variable,
        return None if the node_index is not of an acceptance state.
        """
        try:
            token_name = self.graph.node[node_index]['acceptance']
            return token_name
        except:
            return None

    def draw(self):
        el = get_edge_attributes(self.graph, 'weight')
        pos = circular_layout(self.graph, scale=2)
        draw_networkx(self.graph, pos)

        draw_networkx_edge_labels(self.graph, pos=pos, edge_labels=el)
        plt.show()
