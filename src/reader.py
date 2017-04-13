from nltk import tokenize


class Reader:
    def __init__(self, filename):
        self.filename = filename

    def getTokens(self):
        file = open(self.filename)
        content = file.read()

        # TODO: if input '> =', tree bank will ignore spaces
        tokens = tokenize.TreebankWordTokenizer().tokenize(content)

        relops = ['!=', '>=', '<=']

        for i in range(len(tokens)):
            try:
                new_token = tokens[i] + tokens[i + 1]
            except IndexError:
                pass

            if new_token in relops:
                tokens[i] = new_token
                del tokens[i + 1]

        return tokens
