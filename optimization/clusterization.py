from index.inverted_index import InvertedIndex

import random
import math

from bitstring import BitArray as _BitArray

# hack to make BitArray hashable
class BitArray(_BitArray):
    def __hash__(self):
        return id(self)

def _getCosinusBetweenVectors(vector1, vector2):
    scalar_product = vector1 & vector2
    return (1.0 * scalar_product.count(True)) / (math.sqrt(1.0 * vector1.count(True)) * math.sqrt(1.0 * vector2.count(True)))

def _getDocumentVectors(index, documents_count):
    words_count = index.getUniqueWordsCount()
    vectors = [(doc_id, BitArray(length = words_count)) for doc_id in range(documents_count)]

    words_counter = 0
    for term in index.getDictionary():
        for doc in index.getDocumentsList(term):
            vectors[doc][1].set(True, words_counter)
        words_counter += 1

    return vectors

def _getLeaders(vectors):
    return random.sample(vectors, int(round(math.sqrt(1.0 * len(vectors)))))

def _getNearestLeader(vector, leaders):
    max_cosinus = 0.0
    nearest_leader = None
    for l in leaders:
        cur_cos = _getCosinusBetweenVectors(vector[1], l[1])
        if cur_cos >= max_cosinus:
            max_cosinus = cur_cos
            nearest_leader = l

    return nearest_leader

def _distributeVectorsByClusters(vectors, leaders, use_id):
    clusters = dict((leader if use_id is False else leader[0], []) for leader in leaders)
    for v in vectors:
        if v in leaders:
            continue
        else:
            if use_id is False:
                clusters[_getNearestLeader(v, leaders)].append(v)
            else:
                clusters[_getNearestLeader(v, leaders)[0]].append(v[0])

    return clusters

def getClustersForDocuments(index, documents_count, use_doc_id):
    vectors = _getDocumentVectors(index, documents_count)
    return _distributeVectorsByClusters(vectors, _getLeaders(vectors), use_doc_id)