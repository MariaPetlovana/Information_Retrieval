import xml.etree.ElementTree as ET

from helpers.parser import Parser

class Fb2File:
    def __init__(self, file_name):
        self.file_name = file_name
        self.namespace = ''
        self.tree = None
        self.context = None
        self.root = None
        self.elem = None
        self.tags = ['p', 'strong', 'emphasis']
        self.parser = Parser()

    def open(self):
        self.tree = ET.iterparse(self.file_name)
        self.contex = iter(self.tree)
        event, self.root = next(self.contex)
        self.namespace = self.parser.getNamespace(self.root)

        for index in range(len(self.tags)):
            self.tags[index] = self.namespace + self.tags[index]

    def close(self):
        del self.context

    def canRead(self):
        try:
            event, self.elem = next(self.contex)
        except StopIteration:
            return False
        return True

    def getText(self):
        words = list()

        if self.elem.tag in self.tags:
            paragraph = self.elem.text
            if paragraph != None:
                words = self.parser.separateWords(paragraph)

        self.elem.clear()
        return words