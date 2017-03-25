def is_letter(char):
    """
    Checks whether a certain char is a letter
    >>> is_letter('B')
    True
    >>> is_letter('b')
    True
    >>> is_letter('#')
    False
    """
    return 'A' <= char <= 'z'


def string_to_priority_hash(string):
    """
    Returns a priority hash from a string with the highest priority given
     to the first character and the lowest given to the last character

    >>> string_to_priority_hash('ab')['a']
    2
    >>> string_to_priority_hash('ab')['b']
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
