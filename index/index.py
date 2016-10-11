from helpers.utils import QueryType

from collections import OrderedDict

class Index(object):
    def __init__(self, use_ordered_dict = False):
        self.index = dict() if not use_ordered_dict else OrderedDict()
        self.execute_query = {QueryType.AND : self._and,
                              QueryType.OR :  self._or,
                              QueryType.NOT : self._not
                              }

    def addToIndex(self, term, file_index):
        return

    def addToIndex(self, term, file_index, word_pos):
        return

    def getDictionary(self):
        return sorted(self.index)

    def search(self, query_list, query_type):
        return self.execute_query[query_type](query_list)

    def _and(self, query_list):
        return list()

    def _or(self, query_list):
        return list()

    def _not(self, query_list):
        return list()