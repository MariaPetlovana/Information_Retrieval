from helpers.parser import*

from index.index import Index

class CoordinateIndex(Index):
    def __init__(self):
        Index.__init__(self)

    def addToIndex(self, term, file_index, word_pos):
        value = self.index.get(term, dict())
        if file_index not in list(value.keys()):
            value[file_index] = [word_pos]
        else:
            file_positions = value.get(file_index, list())
            file_positions.append(word_pos)
            value[file_index] = file_positions

        self.index[term] = value

    def findPhraseInRange(self, query_dict):
        if len(list(query_dict.keys())) == 0:
            return dict()

        documents_with_poses = dict()
        for key, value in query_dict.items():
            if not documents_with_poses:
                documents_with_poses = self.findPhrase(separateWords(key))
            else:
                documents_with_poses = self.__intersect(documents_with_poses, self.findPhrase(separateWords(key)), int(value), False)

        return documents_with_poses

    def findPhrase(self, query_list):
        if len(query_list) == 0:
            return dict()

        documents_with_poses = self.index.get(query_list[0], dict())
        for i in range(1, len(query_list)):
            documents_with_poses = self.__intersect(documents_with_poses, self.index.get(query_list[i], dict()))

        return documents_with_poses

    def __intersect(self, word1_docs_pos, word2_docs_pos, k = 1, is_ordered = True):
        res = dict()

        word1_docs = list(word1_docs_pos.keys())
        word2_docs = list(word2_docs_pos.keys())

        i = 0
        j = 0
        while i < len(word1_docs) and j < len(word2_docs):
            if word1_docs[i] == word2_docs[j]:
                pos_index_i = 0
                pos_index_j = 0

                while pos_index_i < len(word1_docs_pos[word1_docs[i]]) and pos_index_j < len(word2_docs_pos[word2_docs[j]]):
                    if abs(word2_docs_pos[word2_docs[j]][pos_index_j] - word1_docs_pos[word1_docs[i]][pos_index_i]) <= k:
                        if not is_ordered or word2_docs_pos[word2_docs[j]][pos_index_j] > word1_docs_pos[word1_docs[i]][pos_index_i]:
                            cur_doc_positions = res.get(word1_docs[i], list())
                            cur_doc_positions.append(word2_docs_pos[word2_docs[j]][pos_index_j])
                            res[word1_docs[i]] = cur_doc_positions

                            pos_index_i += 1

                        pos_index_j += 1
                    else:
                        if word2_docs_pos[word2_docs[j]][pos_index_j] < word1_docs_pos[word1_docs[i]][pos_index_i]:
                            pos_index_j += 1
                        else:
                            pos_index_i += 1

                i += 1
                j += 1
            else:
                if word1_docs[i] < word2_docs[j]:
                    i += 1
                else:
                    j += 1

        return res