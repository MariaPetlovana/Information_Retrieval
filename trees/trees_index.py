from trees.trees_index_base import*
from trees.trie import Trie

class TreesIndex(TreesIndexBase):
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

        wildcards_number = query.count('*')

        # queries with more than 2 '*' are not supported
        if wildcards_number > 2:
            return list()

        if wildcards_number == 1:
            if query[0] == '*':
                return sorted(self.__reverseWords(self.suffix_tree.getWordsStartingFrom(query[::-1])))

            if query[len(query) - 1] == '*':
                return sorted(self.prefix_tree.getWordsStartingFrom(query))

        prefix_words = self.prefix_tree.getWordsStartingFrom(query)
        suffix_words = self.__reverseWords(self.suffix_tree.getWordsStartingFrom(query[::-1]))
        words_from_trees = list(set.intersection(set(prefix_words), set(suffix_words)))

        if wildcards_number == 2:
            wildcard_indices = self.getIndicesOfChar(query, '*')
            middle_word = query[(wildcard_indices[0] + 1) : wildcard_indices[1]]
            suffix_len = len(query[(wildcard_indices[1] + 1):])
            return sorted(self.getAllWordsWithMiddleWord(words_from_trees, middle_word, wildcard_indices[0], suffix_len))

        return sorted(words_from_trees)

    def __reverseWords(self, words):
        for i in range(len(words)):
            words[i] = words[i][::-1]
        return words