import re
import shlex

from collections import OrderedDict

from helpers.utils import QueryType

def parseQueryWithRanges(text):
    res = OrderedDict()
    splitted_query = shlex.split(text)
    for pair in splitted_query:
        splitted = pair.split('/')
        res[splitted[0].lower()] = int(splitted[1]) if len(splitted) == 2 else 0

    return OrderedDict(reversed(list(res.items())))

def getTextInRoundBrackets(text):
    return re.findall('\((.*?)\)', text)

def parseQuery(query):
    and_pattern = re.compile('\([\w]*\) and \([\w]*\)')
    if and_pattern.match(query):
        return (getTextInRoundBrackets(query), QueryType.AND)

    or_pattern = re.compile('\([\w]*\) or \([\w]*\)')
    if or_pattern.match(query):
        return (getTextInRoundBrackets(query), QueryType.OR)

    not_pattern = re.compile('\([\w]*\) not \([\w]*\)')
    if not_pattern.match(query):
        return (getTextInRoundBrackets(query), QueryType.NOT)

    return ([], QueryType.UNDEFINED)

def separateWords(text):
    splitter = re.compile('[^a-zA-Z]*')
    return list([s.lower() for s in splitter.split(text) if s != ''])

def getNamespace(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''

def checkIfStrinIsWord(string):
    word_pattern = re.compile('[\w]*')
    return word_pattern.match(string)

def getIndicesOfChar(str, char):
    return [i for i, letter in enumerate(str) if letter == char]

