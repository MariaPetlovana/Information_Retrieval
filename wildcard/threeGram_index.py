from helpers.parser import*

from orderedset import OrderedSet

class ThreeGramIndex(object):
    def __init__(self):
        self.index = dict()

    def addWord(self, word):
        threeGrams = self.__splitTo3grams(word)

        for threeGram in threeGrams:
            words = self.index.get(threeGram, OrderedSet())
            words.add(word)
            self.index[threeGram] = words

    def find(self, query):
        if not query:
            return list()

        if '*' not in query:
            return query

        threeGrams = self.__splitTo3grams(query, True)
        words = sorted(self.index.get(threeGrams[0], OrderedSet()))

        for i in range(1, len(threeGrams)):
            if not words:
                return list()

            words &= self.index.get(threeGrams[i], OrderedSet())

        return list(words)

    def __splitTo3grams(self, word, is_query = False):
        threeGrams = OrderedSet()
        first_threeGram = word[0:2]
        if first_threeGram.find('*') == -1:
            threeGrams.add('$' + first_threeGram)

        for i, j in zip(range(len(word) - 3), range(3, len(word))):
            threeGram = word[i:j]
            if is_query and threeGram.find('*') != -1:
                continue
            threeGrams.add(threeGram)

        last_threeGram = word[(len(word) - 2):len(word)]
        if last_threeGram.find('*') == -1:
            threeGrams.add(last_threeGram + '$')
        return threeGrams
