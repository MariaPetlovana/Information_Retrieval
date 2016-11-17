import os.path

def getQueryDocumentsMapping(input_directory, queries_ids):
    test_keys_file = ""
    query_doc_map = dict()

    for root, dirs, files in os.walk(input_directory):
        for f in files:
            fullpath = os.path.join(root, f)
            if os.path.basename(fullpath) == 'cranqrel':
                test_keys_file = fullpath
                break

    with open(test_keys_file, 'r') as f:
        for line in f:
            queryId_and_docs = [int(n) for n in line.split()]
            relevant_docs_list = query_doc_map.get(queryId_and_docs[0], list())
            relevant_docs_list.append(queryId_and_docs[1])
            query_doc_map[queries_ids[queryId_and_docs[0] - 1]] = relevant_docs_list
        f.close()

    return query_doc_map
