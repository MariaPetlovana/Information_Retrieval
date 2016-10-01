from trees.trie import Trie

ENGLISH_ALPHABET_WORDS_NUMBER = 26

class TreesIndex(object):
    def __init__(self):
        self.suffix_tree = Trie(ENGLISH_ALPHABET_WORDS_NUMBER)
        self.prefix_tree = Trie(ENGLISH_ALPHABET_WORDS_NUMBER)

    def addWord(self, word):
        self.suffix_tree.addWord(word[::-1])
        self.prefix_tree.addWord(word)

    def find(self, query):
        if not query:
            return list()

        if '*' not in query:
            return query

        if query.count('*') == 1:
            if query[0] == '*':
                return sorted(self.__reverseWords(self.suffix_tree.getWordsStartingFrom(query[::-1])))

            if query[len(query) - 1] == '*':
                return sorted(self.prefix_tree.getWordsStartingFrom(query))

            prefix_words = self.prefix_tree.getWordsStartingFrom(query)
            suffix_words = self.__reverseWords(self.suffix_tree.getWordsStartingFrom(query[::-1]))
            return list(set.intersection(set(prefix_words), set(suffix_words)))

    def __reverseWords(self, words):
        for i in range(len(words)):
            words[i] = words[i][::-1]
        return words
