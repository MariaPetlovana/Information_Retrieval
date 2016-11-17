from bitstring import BitArray
import os
from pickle import dump

NUMBER_OF_BITS_IN_BYTE = 8
DICTIONARY_FILE = "dictionary.bin"
POSTINGS_FILE = "postings.bin"

class Compressor(object):
    def __init__(self, block_size, index):
        self.block_size = block_size
        self.index = index
        self.compressed_dict = ""
        self.table = dict()

    def compress(self):
        dictionary = self.index.getDictionary()
        cur_dict_pos = 0
        for i in range(len(dictionary)):
            self.__addWordToTable(i, dictionary[i], cur_dict_pos)
            add_to_compressed_dict = "{}{}".format(len(dictionary[i]), dictionary[i])
            cur_dict_pos += len(add_to_compressed_dict)
            self.compressed_dict += add_to_compressed_dict

    def save(self, output_dir):
        dictionary_file = output_dir + "\\" + DICTIONARY_FILE
        posting_file = output_dir + "\\" + POSTINGS_FILE
        os.makedirs(os.path.dirname(dictionary_file), exist_ok = True)
        os.makedirs(os.path.dirname(posting_file), exist_ok = True)

        with open(dictionary_file, 'wb') as dict_file, open(posting_file, 'wb') as docs_file:
            for index, data in self.table.items():
                dict_file.write(bytes(index))
                if data[0] is not None:
                    dict_file.write(bytes(data[0]))
                docs_file.write(bytes(index))
                data[1].tofile(docs_file)

            dict_file.close()
            docs_file.close()

    def __addWordToTable(self, word_number, word, cur_dict_pos):
        docs_list = self.index.index[word][1]
        self.table[word_number] = (None if word_number % self.block_size != 0 else cur_dict_pos,
                                   self.__compressDocsList(docs_list))

    def __compressDocsList(self, docs_list):
        interval_start = docs_list[0]
        compressed_list = self.__getGammaCode(interval_start)

        for i in range(1, len(docs_list)):
            compressed_list = BitArray().join([compressed_list, self.__getGammaCode(docs_list[i] - interval_start)])
            interval_start = docs_list[i]

        return compressed_list

    def __getGammaCode(self, number):
        offset = self.__getOffset(number)
        len = BitArray(uint = 1, length = 1) if offset is None else self.__getLength(offset)
        return BitArray().join(len if offset is None else [len, offset])

    def __getOffset(self, number):
        bit_len = number.bit_length() - 1
        number = number ^ (1 << (number.bit_length() - 1))
        return None if not bit_len \
            else BitArray(uint = number, length = (bit_len // NUMBER_OF_BITS_IN_BYTE) + (bit_len % NUMBER_OF_BITS_IN_BYTE))

    def __getLength(self, offset_bitarray):
        len = BitArray(length = (offset_bitarray.length + 1))
        len.invert()
        return len << 1
