from enum import Enum

class QueryType(Enum):
    AND, OR, NOT = range(3)