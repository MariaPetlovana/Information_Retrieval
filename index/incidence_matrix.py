from index.index import Index

from helpers.utils import QueryType

class IncidenceMatrix(Index):
    def __init__(self, files_count):
        Index.__init__(self)
        self.execute_query = {QueryType.AND : self.__and,
                              QueryType.OR :  self.__or,
                              QueryType.NOT : self.__not
                              }
        self.files_count = files_count
        self.default_value = list("0" * self.files_count)

    def addToIndex(self, term, file_index):
        value = self.index.get(term, list(self.default_value))

        if value[file_index] is '0':
            value[file_index] = '1'

        self.index[term] = value

    def __and(self, query_list, is_inverse_term_docs_presence_list = False):
        res = self.__getIntersection(query_list, is_inverse_term_docs_presence_list)
        return self.__getDocumentsIndicesList(res)

    def __or(self, query_list):
        res = list(self.default_value)

        for term in query_list:
            value = self.index.get(term, list(self.default_value))
            for i in range(self.files_count):
                if value[i] == '1':
                    res[i] = '1'

        return self.__getDocumentsIndicesList(res)

    def __not(self, query_list):
        return self.__and(query_list, True)

    def __getReverseString(self, string):
        res = list(self.default_value)

        for i in range(len(string)):
            res[i] = '0' if string[i] == '1' else '1'

        return res

    def __getIntersection(self, query_list, is_inverse_term_docs_presence_list):
        res = list(self.index.get(query_list[0], list(self.default_value)))

        value = list(self.index.get(query_list[1], list(self.default_value)))
        if is_inverse_term_docs_presence_list is True:
            value = self.__getReverseString(value)

        for i in range(self.files_count):
            if res[i] != value[i]:
                res[i] = '0'

        return res

    def __getDocumentsIndicesList(self, term_documents_presence_list):
        documents_indices_list = list()
        for i in range(self.files_count):
            if term_documents_presence_list[i] == '1':
                documents_indices_list.append(i)

        return documents_indices_list