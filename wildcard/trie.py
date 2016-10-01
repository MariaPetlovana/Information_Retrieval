from wildcard.tree import Tree

class Trie(object):
    def __init__(self, letters_number):
        self.root = Tree(letters_number)

    def addWord(self, word):
        cur_node = self.root

        for letter in word:
            if not cur_node.doesTransitExist(letter):
                cur_node.addTransit(letter)

            cur_node = cur_node.getNext(letter)

        cur_node.is_word_end = True

    def __collectAllWordsOfSubtree(self, subtree, cur_word):
        words = list()

        if subtree.is_word_end:
            words.append(str(cur_word))

        for transit_index in range(subtree.transitions_number):
            transit = subtree.transits[transit_index]
            if not transit:
                continue

            word = cur_word + str(chr(ord('a') + transit_index))
            words.extend(self.__collectAllWordsOfSubtree(transit, word))

        return words

    def getWordsStartingFrom(self, word):
        cur_node = self.root
        words_prefix = ""

        for letter in word:
            if letter == '*':
                break

            # there is no such word in trie
            if not cur_node.doesTransitExist(letter):
                return list()

            words_prefix += letter
            cur_node = cur_node.getNext(letter)

        return self.__collectAllWordsOfSubtree(cur_node, words_prefix)

