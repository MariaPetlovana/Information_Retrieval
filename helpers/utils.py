from enum import Enum
import os.path

class QueryType(Enum):
    AND, OR, NOT, UNDEFINED = range(4)

class Zone(Enum):
    TITLE, ANNOTATION, BODY = range(3)

def getAllFilesWithExt(root_dir, ext):
    match_files = []

    for root, dirs, files in os.walk(root_dir):
        for f in files:
            fullpath = os.path.join(root, f)
            if os.path.splitext(fullpath)[1] == ext:
                match_files.append(fullpath)

    return match_files