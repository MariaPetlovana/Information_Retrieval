class Tree(object):
    def __init__(self, letters_number):
        self.is_word_end = False
        self.transitions_number = letters_number
        self.transits = [None] * self.transitions_number

    def addTransit(self, letter):
        self.transits[ord(letter) - ord('a')] = Tree(self.transitions_number)

    def doesTransitExist(self, letter):
        return self.transits[ord(letter) - ord('a')] != None

    def getNext(self, letter):
        return self.transits[ord(letter) - ord('a')]