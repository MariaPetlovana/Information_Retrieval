from enum import Enum

from fb2io.fb2io import Fb2io
from fb2io.fb2File import Fb2File

from helpers.utils import QueryType

from index.index import Index
from index.incidence_matrix import IncidenceMatrix
from index.inverted_index import InvertedIndex
from index.coordinate_index import CoordinateIndex
from index.two_word_index import TwoWordIndex
from index.index_manager import IndexManager

from wildcard.trees_index import TreesIndex
from wildcard.permutative_index import PermutativeIndex
from wildcard.threeGram_index import ThreeGramIndex

def phraseSearchScenario(fb2_directory):
    fb2io = Fb2io(fb2_directory)
    fb2_files = fb2io.getFb2Files()

    file_counter = 0
    incidence_matrix = IncidenceMatrix(len(fb2_files))
    coordinate_index = CoordinateIndex()
    inverted_index = InvertedIndex()
    two_word_index = TwoWordIndex(inverted_index)

    for file in fb2_files:
        words_counter = 0
        f = Fb2File(file)
        f.open()
        while f.canRead():
            words = f.getText()
            for word in words:
                inverted_index.addToIndex(word, file_counter, words_counter)
                coordinate_index.addToIndex(word, file_counter, words_counter)
                two_word_index.addToIndex(word, file_counter)
                words_counter += 1

        f.close()
        file_counter += 1

    result_file = open(fb2_directory + "\\dictionary.txt", "w+");
    for word in coordinate_index.getDictionary():
        result_file.write(word + "\n")
    result_file.close()

    index_manager = IndexManager(coordinate_index, two_word_index)

    print("Please input a phrase to search. Press Q to quit")

    while True:
        user_input = input()
        if user_input.lower() == "q":
            break

        documents_indices = index_manager.find(user_input)

        if not documents_indices:
            print("There are no documents where all the query words are present")
        else:
            for index in documents_indices:
                print(fb2_files[index])
                if type(documents_indices) is dict:
                    for pos in documents_indices[index]:
                        print(pos)

def jokerSearchScenario(fb2_directory):
    fb2io = Fb2io(fb2_directory)
    fb2_files = fb2io.getFb2Files()

    file_counter = 0
    inverted_index = InvertedIndex()

    trees_index = TreesIndex()
    permutative_index = PermutativeIndex()
    threeGram_index = ThreeGramIndex()

    for file in fb2_files:
        words_counter = 0
        f = Fb2File(file)
        f.open()
        while f.canRead():
            words = f.getText()
            for word in words:
                inverted_index.addToIndex(word, file_counter, words_counter)

        f.close()
        file_counter += 1

    for term in inverted_index.getDictionary():
        #trees_index.addWord(term)
        #permutative_index.addWord(term)
        threeGram_index.addWord(term)

    print("Please input a query with wildcard. Press Q to quit")

    while True:
        user_input = input()
        if user_input.lower() == "q":
            break

        #words = trees_index.find(user_input)
        #words = permutative_index.find(user_input)
        words = threeGram_index.find(user_input)

        if not words:
            print("There are no documents where all the query words are present")
        else:
            for word in words:
                documents_indices = inverted_index.index[word][1]
                docs = list()

                for index in documents_indices:
                    docs.append(fb2_files[index])

                print(word, docs)

if __name__ == "__main__":
    fb2_directory = "E:\\books1"
    jokerSearchScenario(fb2_directory)
