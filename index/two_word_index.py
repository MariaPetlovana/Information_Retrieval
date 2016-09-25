from index.index import Index

class TwoWordIndex(Index):
    def __init__(self):
        Index.__init__(self)
        self.last_word = ''

    def addToIndex(self, word, file_index):
        if self.last_word == '':
            self.last_word = word
            return

        term = self.last_word + ' ' + word
        self.last_word = word

        value = self.index.get(term, list())
        if file_index not in value:
            value.append(file_index)
        self.index[term] = value

    def findPhrase(self, query_list):
        if len(query_list) < 2:
            return list()

        term = query_list[0] + ' ' + query_list[1]
        documents = self.index.get(term, list())
        for i in range(2, len(query_list)):
            documents = self.__and(documents, self.index.get(query_list[i - 1] + ' ' + query_list[i], list()))

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