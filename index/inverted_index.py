from index.index import Index

from helpers.utils import QueryType

class InvertedIndex(Index):
    def __init__(self):
        Index.__init__(self)
        self.execute_query = {QueryType.AND : self.__and,
                              QueryType.OR :  self.__or,
                              QueryType.NOT : self.__not
                              }

    def getWordIndex(self, term):
        return self.index.get(term, (-1, list()))[0]

    def addToIndex(self, term, file_index, word_pos):
        value = self.index.get(term, (word_pos, list()))
        if file_index not in value[1]:
            value[1].append(file_index)
        self.index[term] = value

    def __and(self, query_list):
        res = list()
        value1 = self.index.get(query_list[0], (-1, list()))
        value2 = self.index.get(query_list[1], (-1, list()))

        i = 0
        j = 0
        while i < len(value1[1]) and j < len(value2[1]):
            if value1[1][i] == value2[1][j]:
                res.append(value1[1][i])
                i += 1
                j += 1
            else:
                if value1[1][i] < value2[1][j]:
                    i += 1
                else:
                    j += 1

        return res

    def __or(self, query_list):
        res = list()
        value1 = self.index.get(query_list[0], (-1, list()))
        value2 = self.index.get(query_list[1], (-1, list()))

        i = 0
        j = 0
        while i < len(value1[1]) and j < len(value2[1]):
            if value1[1][i] == value2[1][j]:
                res.append(value1[1][i])
                i += 1
                j += 1
            else:
                if value1[1][i] < value2[1][j]:
                    res.append(value1[1][i])
                    i += 1
                else:
                    res.append(value2[1][j])
                    j += 1

        while i < len(value1[1]):
            res.append(value1[1][i])
            i += 1

        while j < len(value2[1]):
            res.append(value2[1][j])
            j += 1

        return res

    def __not(self, query_list):
        res = list()
        value1 = self.index.get(query_list[0], (-1, list()))
        value2 = self.index.get(query_list[1], (-1, list()))

        i = 0
        j = 0
        while i < len(value1[1]) and j < len(value2[1]):
            if value1[1][i] == value2[1][j]:
                i += 1
                j += 1
            else:
                if value1[1][i] < value2[1][j]:
                    res.append(value1[1][i])
                    i += 1
                else:
                    j += 1

        while i < len(value1[1]):
            res.append(value1[1][i])
            i += 1

        return res