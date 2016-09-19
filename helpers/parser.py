import re

from helpers.utils import QueryType

class Parser(object):
    def getTextInRoundBrackets(self, text):
        return re.findall('\((.*?)\)', text)

    def parseQuery(self, query):
        and_pattern = re.compile('\([\w]*\) and \([\w]*\)')
        if and_pattern.match(query):
            return (self.getTextInRoundBrackets(query), QueryType.AND)

        or_pattern = re.compile('\([\w]*\) or \([\w]*\)')
        if or_pattern.match(query):
            return (self.getTextInRoundBrackets(query), QueryType.OR)

        not_pattern = re.compile('\([\w]*\) not \([\w]*\)')
        if not_pattern.match(query):
            return (self.getTextInRoundBrackets(query), QueryType.NOT)

    def separateWords(self, text):
        splitter = re.compile('[^a-zA-Z]*')
        return list([s.lower() for s in splitter.split(text) if s != ''])

    def getNamespace(self, element):
        m = re.match('\{.*\}', element.tag)
        return m.group(0) if m else ''

    def checkIfStrinIsWord(self, string):
        word_pattern = re.compile('[\w]*')
        return word_pattern.match(string)
