import xml.etree.ElementTree as ET

from helpers.parser import*
from helpers.utils import Zone

class Fb2File:
    def __init__(self, file_name):
        self.file_name = file_name
        self.namespace = ''
        self.tree = None
        self.context = None
        self.root = None
        self.elem = None
        self.zone_retrieval = False
        self.body_root_passed = False
        self.body_tags = ['p', 'strong', 'emphasis']
        self.zones = ['genre', 'author', 'book-title', 'title', 'annotation']
        self.tag_zone_map = { 'genre' :      Zone.TITLE,
                              'author' :     Zone.TITLE,
                              'book-title' : Zone.TITLE,
                              'title' :      Zone.TITLE,
                              'annotation' : Zone.ANNOTATION
                              }

    def open(self, use_zones = False):
        self.zone_retrieval = use_zones
        self.tree = ET.iterparse(self.file_name, events = ("start", "end"))
        self.context = iter(self.tree)
        event, self.root = next(self.context)
        self.namespace = getNamespace(self.root)

        for index in range(len(self.body_tags)):
            self.body_tags[index] = self.namespace + self.body_tags[index]

        for index in range(len(self.zones)):
            self.zones[index] = self.namespace + self.zones[index]

    def close(self):
        del self.context

    def canRead(self):
        while True:
            try:
                event, self.elem = next(self.context)
                if event == "start":
                    if 'body' in self.elem.tag:
                        self.body_root_passed = True
                else:
                    return True
            except StopIteration:
                return False

    def getText(self):
        words = list()

        if not self.zone_retrieval:
            return self.__getTextFromSingleTag()

        if self.body_root_passed is True:
            return self.__getTextFromSingleTag()

        return self.__getTextFromChildren()

    def __getTextFromSingleTag(self):
        words = list()

        if self.elem.tag in self.body_tags:
            paragraph = self.elem.text
            if paragraph != None:
                words = separateWords(paragraph)

        self.elem.clear()
        return words if not self.zone_retrieval else Zone.BODY, words

    def __getTextFromChildren(self):
        words = []

        if self.elem.tag in self.zones:
            for child in self.elem:
                text = child.text
                if text != None:
                    words.extend(separateWords(text))

            text = self.elem.text
            if text != None:
                words.extend(separateWords(text))
            self.elem.clear()
            zone = self.tag_zone_map.get(self.elem.tag, -1)
            if zone != -1:
                return self.tag_zone_map[self.elem.tag], words

            self.tag_zone_map[self.elem.tag] = \
                self.tag_zone_map.pop(self.elem.tag[self.elem.tag.find(self.namespace) + len(self.namespace):])
            return self.tag_zone_map[self.elem.tag], words

        return -1, []
