def getTruePositiveRes(returned_docs, key_docs):
    return [doc for doc in returned_docs if doc in key_docs]

def getFalsePositiveRes(returned_docs, true_positive_docs):
    return [doc for doc in returned_docs if doc not in true_positive_docs]

def getTrueNegativeRes(returned_docs, key_docs, all_docs):
    not_relevant_docs = [doc for doc in all_docs if doc not in key_docs]
    return [doc for doc in not_relevant_docs if doc not in returned_docs]

def getFalseNegativeRes(returned_docs, key_docs):
    relevant_docs = getTruePositiveRes(returned_docs, key_docs)
    return [doc for doc in key_docs if doc not in relevant_docs]

def calculatePrecision(returned_docs, key_docs):
    return (1.0 * len(getTruePositiveRes(returned_docs, key_docs))) / len(returned_docs)

def calculateRecall(returned_docs, key_docs):
    relevant_docs = getTruePositiveRes(returned_docs, key_docs)
    false_negative_docs = getFalseNegativeRes(returned_docs, key_docs)
    return (1.0 * len(relevant_docs)) / (len(relevant_docs) + len(false_negative_docs))

def calculateAccuracy(returned_docs, key_docs, all_docs):
    relevant_docs = getTruePositiveRes(returned_docs, key_docs)
    false_negative_docs = getFalseNegativeRes(returned_docs, key_docs)
    true_negative_docs = getTrueNegativeRes(returned_docs, key_docs, all_docs)
    return (1.0 * (len(relevant_docs) + len(true_negative_docs))) / \
           (len(returned_docs) + len(false_negative_docs) + len(true_negative_docs))
