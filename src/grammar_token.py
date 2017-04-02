class GrammarToken:
    def __init__(self, name, regex):
        self.regex = regex
        self.name = name

    def __repr__(self):
        return "Name: %s  Regex: %s" % (self.name, self.regex)
