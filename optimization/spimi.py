from fb2io.fb2io import Fb2io
from fb2io.fb2File import Fb2File

from index.inverted_index import InvertedIndex

from helpers.utils import*

from orderedset import OrderedSet

import ast
import operator

BLOCK_NAME_PATTERN = "block{}.txt"

def getIndexTriplesFromDoc(file_index, words, word_pos_start):
	return [ (term, file_index, word_pos_start + pos) for pos, term in enumerate(words) ]

def generateTokenStream(fb2_directory, block_size):
    token_stream = []

    fb2io = Fb2io(fb2_directory)
    fb2_files = fb2io.getFb2Files()

    file_counter = 0

    for file in fb2_files:
        words_counter = 0
        block_index = 0
        f = Fb2File(file)
        f.open()
        while f.canRead():
            words = f.getText()
            token_stream.extend(getIndexTriplesFromDoc(file_counter, words, words_counter))
            if len(token_stream) >= block_size:
                yield block_index, token_stream
                block_index += 1
                token_stream = token_stream[block_size:]
            words_counter += len(words)

        f.close()
        file_counter += 1

    if token_stream:
        yield block_index, token_stream

def spimiInvert(input_dir, block_index, token_stream):
	output_file = (input_dir + "\\" + BLOCK_NAME_PATTERN).format(block_index)

	inverted_index = InvertedIndex()
	for token in token_stream:
		inverted_index.addToIndex(token[0], token[1], token[2])

	sorted_index = inverted_index.getSortedIndex()

	with open(output_file, 'wt') as f:
		f.write('\n'.join(['{},{}'.format(t, str(sorted_index.index[t][1])) for t in sorted_index.index.keys()]))
	return output_file

def mergeStep(terms_and_docs):
    terms_and_docs.sort()
    res_list = []
    files_to_read_further = []
    term = terms_and_docs[0][0]
    terms_list = [t for t, l, j in terms_and_docs]
    count = terms_list.count(term)
    if count == 1:
        res_list.append((term, terms_and_docs[0][1]))
        files_to_read_further.append(terms_and_docs[0][2])
    else:
        index = terms_list.index(term)
        d_list = OrderedSet()

        for t, l, block_id in terms_and_docs[index:(index + count)]:
            d_list |= l
            files_to_read_further.append(block_id)

        res_list.append((term, list(d_list)))

    return res_list, files_to_read_further

def mergeBlocks(blocks, output_file):
    with open(output_file, 'wt') as index:
        files = [open(b,'rt') for b in blocks]
        res = []
        lines = [None] * len(files)
        files_to_read = list(range(0, len(files)))

        while True:
            for i in range(len(files)):
                if i in files_to_read:
                    lines[i] = files[i].readline()

            if not any(lines):
                break

            terms_and_docs = []
            for i in range(len(lines)):
                if lines[i] != '':
                    terms_and_docs.append(
                        (lines[i][:lines[i].index(',')],
                         ast.literal_eval(lines[i][lines[i].index('['):lines[i].index(']') + 1]),
                         i)
                    )

            merged, read_next = mergeStep(terms_and_docs)
            files_to_read = read_next
            res.extend(merged)

        for term, docs_list in res:
            index.write('{},{}\n'.format(term, docs_list))
        for f in files:
            f.close()

def spimi(input_dir, output_file, block_size = 1 << 16):
    blocks = [spimiInvert(input_dir, block_index, tokens_block)
              for block_index, tokens_block
              in generateTokenStream(input_dir, block_size)]

    mergeBlocks(blocks, output_file)
