from enum import Enum

class QueryType(Enum):
    AND, OR, NOT, UNDEFINED = range(4)