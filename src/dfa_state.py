class DFAState():
    def __init__(self, NFAStates, visited=True):
        self.NFAStates = NFAStates
        self.visited = visited

    def mark_as_visited(self):
        self.visited = True

    def mark_as_not_visited(self):
        self.visited = False

    def is_visited(self):
        return self.visited

    def get_nfa_states(self):
        return self.NFAStates
