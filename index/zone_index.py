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

    def _getFilesList(self, term):
        return list(self.index.get(term, dict()).keys())

    def _and(self, query_list):
        intersected_files = super(ZoneIndex, self)._and(query_list)
        scores = [0.0] * self.files_count

        for f in intersected_files:
            score = self.__getBooleanScore(f, query_list) if len(query_list) == 2 \
                else self.__getRelativeScore(f, query_list)
            scores[f] = self.__weightedZone(score)

        return scores

    def __weightedZone(self, scores):
        weights = []
        for i in range(ZONES_NUMBER):
            weights.append(self.zone_weights[Zone(i)] * scores[i])
        return sum(weights)

    def __getRelativeScore(self, doc_id, query_list):
        zones_coeficients = []

        for z in Zone:
            zone_contain_terms_counter = len(query_list)

            for term in query_list:
                zones = self.index[term][doc_id]
                if z not in zones:
                    zone_contain_terms_counter -= 1
                    break

            zones_coeficients.append((1.0 * zone_contain_terms_counter) / len(query_list))

        return zones_coeficients

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