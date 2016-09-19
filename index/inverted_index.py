from index.index import Index

from helpers.utils import QueryType

class InvertedIndex(Index):
    def __init__(self):
        Index.__init__(self)
        self.execute_query = {QueryType.AND : self.__and,
                              QueryType.OR :  self.__or,
                              QueryType.NOT : self.__not
                              }

    def addToIndex(self, term, file_index):
        value = self.index.get(term, list())
        if file_index not in value:
            value.append(file_index)
        self.index[term] = value

    def __and(self, query_list):
        res = list()
        value1 = self.index.get(query_list[0], list())
        value2 = self.index.get(query_list[1], list())

        i = 0
        j = 0
        while i < len(value1) and j < len(value2):
            if value1[i] == value2[j]:
                res.append(value1[i])
                i += 1
                j += 1
            else:
                if value1[i] < value2[j]:
                    i += 1
                else:
                    j += 1

        return res

    def __or(self, query_list):
        res = list()
        value1 = self.index.get(query_list[0], list())
        value2 = self.index.get(query_list[1], list())

        i = 0
        j = 0
        while i < len(value1) and j < len(value2):
            if value1[i] == value2[j]:
                res.append(value1[i])
                i += 1
                j += 1
            else:
                if value1[i] < value2[j]:
                    res.append(value1[i])
                    i += 1
                else:
                    res.append(value2[j])
                    j += 1

        while i < len(value1):
            res.append(value1[i])
            i += 1

        while j < len(value2):
            res.append(value2[j])
            j += 1

        return res

    def __not(self, query_list):
        res = list()
        value1 = self.index.get(query_list[0], list())
        value2 = self.index.get(query_list[1], list())

        i = 0
        j = 0
        while i < len(value1) and j < len(value2):
            if value1[i] == value2[j]:
                i += 1
                j += 1
            else:
                if value1[i] < value2[j]:
                    res.append(value1[i])
                    i += 1
                else:
                    j += 1

        while i < len(value1):
            res.append(value1[i])
            i += 1

        return res