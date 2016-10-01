from wildcard.trees_index_base import*
from wildcard.trie import Trie

from helpers.parser import*

class PermutativeIndex(TreesIndexBase):
    def __init__(self):
        self.permutative_tree = Trie(ENGLISH_ALPHABET_WORDS_NUMBER + 1) # plus 1 fictive character

    def addWord(self, word):
        permutations = self.__getAllCyclicPermutations(word)
        for p in permutations:
            self.permutative_tree.addWord(p)

    def find(self, query):
        if not query:
            return list()

        if '*' not in query:
            return query

        wildcards_number = query.count('*')
        middle_word = ""
        suffix_len = ""

        if wildcards_number > 2:
            return list()

        if wildcards_number == 2:
            wildcard_indices = getIndicesOfChar(query, '*')
            middle_word = query[(wildcard_indices[0] + 1) : wildcard_indices[1]]
            suffix_len = len(query[(wildcard_indices[1] + 1):])

        fictive_char = chr(ord('a') + ENGLISH_ALPHABET_WORDS_NUMBER)
        query += fictive_char
        query = self.__reverseWordTillSymbol(query[:wildcard_indices[0]] + query[wildcard_indices[1]:], '*')

        words_with_fictive_char = self.permutative_tree.getWordsStartingFrom(query)

        res = list()
        for w in words_with_fictive_char:
            res.append(self.__reverseWordTillSymbol(w, fictive_char, True))

        if wildcards_number == 2:
            return sorted(self.getAllWordsWithMiddleWord(res, middle_word, wildcard_indices[0], suffix_len))

        return sorted(res)

    def __getAllCyclicPermutations(self, word):
        permutations = list()
        cur_word = word + chr(ord('a') + ENGLISH_ALPHABET_WORDS_NUMBER) # the next after 'z'
        permutations.append(cur_word)

        w = cur_word
        while True:
            w = w[1:] + w[0]
            permutations.append(w)
            if w == cur_word:
                break

        return permutations

    def __reverseWordTillSymbol(self, word, char, cut_symbol = False):
        while word[len(word) - 1] != char:
            word = word[1:] + word[0]

        return word[:(len(word) - 1)] if cut_symbol else word