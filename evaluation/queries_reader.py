from helpers.parser import*
from helpers.utils import*

from parse import*
import re
from enum import Enum

class Query(object):
    def __init__(self, id):
        self.id = id
        self.query = ""

class QueriesReader(object):
    def __init__(self, queries_dir):
        self.file_name = getAllFilesWithExt(queries_dir, '.qry')[0]
        self.queries = []

    def getQueries(self):
        with open(self.file_name, 'r') as f:
            for line in f:
                cropped_line = line.rstrip('\n')
                id_pattern = re.compile('\.I \d')
                query_pattern = re.compile('\.W')
                if query_pattern.match(cropped_line):
                    continue
                elif id_pattern.match(cropped_line):
                    id = parse(".I {:d}", line)[0]
                    self.queries.append(Query(id))
                else:
                    self.queries[-1].query += line
            f.close()

        return self.queries
