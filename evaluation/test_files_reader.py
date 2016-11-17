from helpers.parser import*

from parse import*
import re
from enum import Enum

class FileItemState(Enum):
    NONE, ID, TITLE, AUTHOR, PUBLISHER, BODY = range(6)

class File(object):
    def __init__(self, id):
        self.id = id
        self.author = ""
        self.title = ""

class TestDataReader(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.files = []

    def getCurrentFileId(self):
        return self.files[-1].id

    def getWords(self):
        cur_state = FileItemState.NONE

        with open(self.file_name, 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                if cur_state == FileItemState.NONE:
                    id_pattern = re.compile('\.I \d')
                    if id_pattern.match(line):
                        id = parse(".I {:d}", line)[0]
                        self.files.append(File(id))
                        cur_state = FileItemState.ID
                elif cur_state == FileItemState.ID:
                    title_pattern = re.compile('\.T')
                    if title_pattern.match(line):
                        cur_state = FileItemState.TITLE
                elif cur_state == FileItemState.TITLE:
                    author_pattern = re.compile('\.A')
                    if author_pattern.match(line):
                        cur_state = FileItemState.AUTHOR
                    else:
                        self.files[-1].title += line
                        yield separateWords(line)
                elif cur_state == FileItemState.AUTHOR:
                    publisher_pattern = re.compile('\.B')
                    if publisher_pattern.match(line):
                        cur_state = FileItemState.PUBLISHER
                    else:
                        self.files[-1].author += line
                        yield separateWords(line)
                elif cur_state == FileItemState.PUBLISHER:
                    body_pattern = re.compile('\.W')
                    if body_pattern.match(line):
                        cur_state = FileItemState.BODY
                    else:
                        yield separateWords(line)
                elif cur_state == FileItemState.BODY:
                    id_pattern = re.compile('\.I \d')
                    if id_pattern.match(line):
                        id = parse(".I {:d}", line)[0]
                        self.files.append(File(id))
                        cur_state = FileItemState.ID
                    else:
                        yield separateWords(line)
            f.close()

        return []
