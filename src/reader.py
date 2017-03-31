from nltk import tokenize


class Reader:
    def __init__(self, filename):
        self.filename = filename

    def getTokens(self):
        file = open(self.filename)
        content = file.read()

        return tokenize.TreebankWordTokenizer().tokenize(content)
