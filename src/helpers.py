def is_letter(char):
    """
    Checks whether a certain char is a letter
    >> is_letter('B')
    True
    >> is_letter('b')
    True
    >> is_letter('#')
    False
    """
    return 'A' <= char <= 'z'


def string_to_priority_hash(string):
    """
    Returns a priority hash from a string with the highest priority given
     to the first character and the lowest given to the last character

    >> string_to_priority_hash('ab')['a']
    2
    >> string_to_priority_hash('ab')['b']
    1
    """
    priority_hash = {}
    priority = len(string)
    for char in string:
        priority_hash[char] = priority
        priority -= 1
    return priority_hash


class Stack:
    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.append(item)

    def peek(self):
        if len(self.list) > 0:
            return self.list[-1]
        else:
            return None

    def pop(self):
        if len(self.list) > 0:
            return self.list.pop()
        else:
            return None

    def empty(self):
        return len(self.list) == 0


def add_concatenation_operator_to_regex(regex):
    """
    This function adds '&' character for explicit concatenation

    >> add_concatenation_operator_to_regex('abc')
    'a&b&c'
    >> add_concatenation_operator_to_regex('a|b|c')
    'a|b|c'
    >> add_concatenation_operator_to_regex('a(bc)*')
    'a&(b&c)*'
    """
    if len(regex) == 1: return regex
    chars = []
    current_char = None
    next_char = None
    for i in range(0, len(regex) - 1):
        current_char = regex[i]
        next_char = regex[i + 1]

        if current_char not in '(+|-\\' and next_char not in '|)*-+':
            chars += [current_char, '&']
        else:
            chars.append(current_char)
    if next_char and current_char:
        # handle last character
        if next_char == ')' or (current_char == ')' and next_char == '*') or \
                (current_char not in '()*+' and next_char not in '()*+|') or current_char == '\\' or \
                                current_char == '*' and next_char not in '()|*' or \
                        next_char == '+':
            chars.append(next_char)
        else:
            chars += ['&', next_char]

    return ''.join(chars)
