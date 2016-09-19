from enum import Enum

from helpers.parser import Parser
from helpers.utils import QueryType

from index.index import Index
from index.incidence_matrix import IncidenceMatrix
from index.inverted_index import InvertedIndex

from fb2io.fb2io import Fb2io
from fb2io.fb2File import Fb2File

if __name__ == "__main__":
    fb2_directory = "E:\\books1"

    fb2io = Fb2io(fb2_directory)
    fb2_files = fb2io.getFb2Files()

    file_counter = 0
    incidence_matrix = IncidenceMatrix(len(fb2_files))
    inverted_index = InvertedIndex()
    parser = Parser()

    for file in fb2_files:
        f = Fb2File(file)
        f.open()
        while f.canRead():
            words = f.getText()
            for word in words:
                incidence_matrix.addToIndex(word, file_counter)
                inverted_index.addToIndex(word, file_counter)

        f.close()
        file_counter += 1

    result_file = open(fb2_directory + "\\dictionary.txt", "w+");
    for word in inverted_index.getDictionary():
        result_file.write(word + "\n")
    result_file.close()

    print("Please input a boolean query in one of the following formats:\n" \
            "(word1) and (word2)\n" \
            "(word1) or (word2)\n" \
            "(word1) not (word2)\n" \
            "To finish work press Q\n")

    while True:
        user_input = input()
        if user_input.lower() == "q":
            break

        parsed_query = parser.parseQuery(user_input.lower())
        wrong_query_message = "Wrong query!\nPlease try again.\n"

        if not parsed_query or len(parsed_query[0]) != 2:
            print(wrong_query_message)
        else:
            is_wrong_query = False
            for term in parsed_query[0]:
                if not term:
                    print(wrong_query_message)
                    is_wrong_query = True
                    break;

            if is_wrong_query is False:
                documents_indices = incidence_matrix.search(parsed_query[0], parsed_query[1])
                documents_indices1 = inverted_index.search(parsed_query[0], parsed_query[1])

                if not documents_indices:
                    print("There are no documents where all the query words are present")
                else:
                    for index in documents_indices:
                        print(fb2_files[index])
                    for index in documents_indices1:
                        print(fb2_files[index])