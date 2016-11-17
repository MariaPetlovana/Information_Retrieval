from helpers.utils import*

class Fb2io:
    def __init__(self, fb2_directory):
        self.fb2_directory = fb2_directory

    def getFb2Files(self):
        return getAllFilesWithExt(self.fb2_directory, '.fb2')

