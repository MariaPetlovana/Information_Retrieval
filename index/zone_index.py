from helpers.utils import Zone
from helpers.parser import*

from index.inverted_index import InvertedIndex

# assume we have 3 zones: title, annotation and body
ZONES_NUMBER = 3

class ZoneIndex(InvertedIndex):
    def __init__(self, files_count):
        InvertedIndex.__init__(self, False)
        self.files_count = files_count
        self.zone_weights = { Zone.TITLE : 0.2,
                              Zone.ANNOTATION : 0.3,
                              Zone.BODY : 0.5
                              }

    def addToIndex(self, term, file_index, zone):
        docs_list = self.index.get(term, dict())
        file_indices_list = list(docs_list.keys())
        if file_index not in file_indices_list:
            docs_list[file_index] = [zone]
        else:
            if zone not in docs_list[file_index]:
                docs_list[file_index].append(zone)

        self.index[term] = docs_list

    def _and(self, query_list):
        query_list = separateWords(query_list)
        scores = [0.0] * self.files_count

        res = list()
        docs_dict1 = self.index.get(query_list[0], dict())
        docs_dict2 = self.index.get(query_list[1], dict())

        i = 0
        j = 0

        files1 = list(docs_dict1.keys())
        files2 = list(docs_dict2.keys())

        while i < len(files1) and j < len(files2):
            if files1[i] == files2[j]:
                boolean_score = self.__getBooleanScore(files1[i], query_list)
                scores[files1[i]] = self.__weightedZone(boolean_score)
                i += 1
                j += 1
            else:
                if files1[i] < files2[j]:
                    i += 1
                else:
                    j += 1

        return scores

    def __weightedZone(self, boolean_score):
        weights = []
        for i in range(ZONES_NUMBER):
            weights.append(self.zone_weights[Zone(i)] * boolean_score[i])
        return sum(weights)

    def __getBooleanScore(self, doc_id, query_list):
        zones_contain_query = []

        for z in Zone:
            zone_contain_all_terms = 1.0

            for term in query_list:
                zones = self.index[term][doc_id]
                if z not in zones:
                    zone_contain_all_terms = 0.0
                    break

            zones_contain_query.append(zone_contain_all_terms)

        return zones_contain_query

    def _or(self, query_list):
        return list() # should not be called

    def _not(self, query_list):
        return list() # should not be called