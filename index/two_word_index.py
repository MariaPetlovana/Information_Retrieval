from index.index import Index

class TwoWordIndex(Index):
    def __init__(self, inverted_index):
        Index.__init__(self)
        self.last_word = ''
        self.inverted_index = inverted_index

    def addToIndex(self, word, file_index):
        if self.last_word == '':
            self.last_word = word
            return

        index_key = (self.inverted_index.getWordIndex(self.last_word), self.inverted_index.getWordIndex(word))
        self.last_word = word

        value = self.index.get(index_key, list())
        if file_index not in value:
            value.append(file_index)
        self.index[index_key] = value

    def findPhrase(self, query_list):
        if len(query_list) < 2:
            return list()

        word1_index = self.inverted_index.getWordIndex(query_list[0])
        if word1_index == -1:
            return list()

        word2_index = self.inverted_index.getWordIndex(query_list[1])
        if word2_index == -1:
            return list()

        index_key = (word1_index, word2_index)
        documents = self.index.get(index_key, list())
        for i in range(2, len(query_list)):
            # no sense to continue intersect documents lists if
            # the temporary result list is already empty
            if not documents:
                break

            word1_index = self.inverted_index.getWordIndex(query_list[i - 1])
            word2_index = self.inverted_index.getWordIndex(query_list[i])

            documents = self.__and(documents, self.index.get((word1_index, word2_index), list()))

        return documents

    def __and(self, cur_docs, docs_to_overlap):
        res = list()
        value1 = cur_docs
        value2 = docs_to_overlap

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