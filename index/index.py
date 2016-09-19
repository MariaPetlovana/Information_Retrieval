from helpers.utils import QueryType

class Index(object):
    def __init__(self):
        self.index = dict()
        self.execute_query = {QueryType.AND : self.__and,
                              QueryType.OR :  self.__or,
                              QueryType.NOT : self.__not
                              }

    def addToIndex(self, term, file_index):
        return

    def getDictionary(self):
        return sorted(self.index)

    def search(self, query_list, query_type):
        return self.execute_query[query_type](query_list)

    def __and(self, query_list):
        return list()

    def __or(self, query_list):
        return list()

    def __not(self, query_list):
        return list()
    