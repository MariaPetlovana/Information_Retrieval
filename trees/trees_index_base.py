ENGLISH_ALPHABET_WORDS_NUMBER = 26

class TreesIndexBase(object):
    def addWord(self, word):
        return

    def find(self, query):
        return list()

    def getIndicesOfChar(self, str, char):
        return [i for i, letter in enumerate(str) if letter == char]

    def getAllWordsWithMiddleWord(self, words, middle_word, start_pos, end_pos_delta):
        res = list()
        for w in words:
            if w.find(middle_word, start_pos, len(w) - end_pos_delta) != -1:
                res.append(w)
        return res