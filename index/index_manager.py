from helpers.parser import*

from index.coordinate_index import CoordinateIndex
from index.two_word_index import TwoWordIndex

class IndexManager(object):
    def __init__(self, coordinate_index, two_word_index):
        self.coordinate_index = coordinate_index
        self.two_word_index = two_word_index

    def find(self, query):
        parsed_query = parseQueryWithRanges(query)
        if not parsed_query:
            return dict()

        if len(list(parsed_query)) == 1: # phrase search
            phrase_list = separateWords(list(parsed_query.keys())[0])
            # if len of phrase is in range [2, 6] -> use two word index
            # else use coordinate index
            return self.two_word_index.findPhrase(phrase_list) \
                if (len(phrase_list) > 1
                    and len(phrase_list) <= 6) \
                else self.coordinate_index.findPhraseInRange(parsed_query)
        else:
            return self.coordinate_index.findPhraseInRange(parsed_query)