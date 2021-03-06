# Information Retrieval Project

This project is written in Python and provides data structures for the search engine creation, such as:

  - *Incidence matrix*
    - word-document boolean table
    - describes presence of each word in each document
    - boolean search
  - *Inverted index*
    - word-document matching
    - for each word holds list of documents where it is present
    - boolean search
  - *Two word index*
    - inverted index by pair of words
    - phrase search
  - *Inverted coordinate index*
    - besides storing documents list, for each document also a list of word's positions in the document is stored
    - phrase search
    - search of word in a range
  - *Suffix and Prefix trees*
    - trie
    - wildcard search
  - *Permutative index*
    - trie
    - wildcard search
  - *3gram index*
    - inverted index
    - 3gram-word matching
  - *Zone index*
    - inverted index
    - term-zone based ranking

Added document-term vectors clusterization based on cosine similarities.

Storage **optimization** is provided:

* [SPIMI](http://nlp.stanford.edu/IR-book/html/htmledition/single-pass-in-memory-indexing-1.html) algorithm is used to improve CPU usage while constructing index for large amount of files. 
* [Blocked storage](http://nlp.stanford.edu/IR-book/html/htmledition/blocked-storage-1.html) and [Gamma codes](http://nlp.stanford.edu/IR-book/html/htmledition/gamma-codes-1.html) compressions are applied to the dictionary and postings lists respectively. 

Also, to work with fb2 files, appropriate classes for reading reading and parsing text from fb2 files are present.

### Tech

There are next requirements to use the project's code:
* Python 3.4.3
* Packages: collections, orderedset, bitstring
