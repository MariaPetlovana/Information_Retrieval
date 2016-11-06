from index.index import Index

from helpers.utils import QueryType

class InvertedIndex(Index):
    def __init__(self, use_ordered_dict = False):
        Index.__init__(self, use_ordered_dict)

    def getUniqueWordsCount(self):
        return len(self.index)

    def getSortedIndex(self):
        sorted_index = InvertedIndex(True)

        for key in sorted(self.index):
            sorted_index.index[key] = self.index[key]

        return sorted_index

    def getWordIndex(self, term):
        return self.index.get(term, (-1, list()))[0]

    def getDocumentsList(self, term):
        return self.index.get(term, (-1, list()))[1]

    def addToIndex(self, term, file_index, word_pos):
        value = self.index.get(term, (word_pos, list()))
        if file_index not in value[1]:
            value[1].append(file_index)
        self.index[term] = value

    def _getFilesList(self, term):
        return self.index.get(term, (-1, list()))[1]

    def _and(self, query_list):
        if not query_list:
            return list()

        if len(query_list) == 1:
            return self._getFilesList(query_list[0])

        res = self._getFilesList(query_list[0])

        for k in range(1, len(query_list)):
            value = self._getFilesList(query_list[k])
            temp_res = list()

            i = 0
            j = 0
            while i < len(value) and j < len(res):
                if value[i] == res[j]:
                    temp_res.append(value[i])
                    i += 1
                    j += 1
                else:
                    if value[i] < res[j]:
                        i += 1
                    else:
                        j += 1

            res = temp_res

        return res

    def _or(self, query_list):
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

    def _not(self, query_list):
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