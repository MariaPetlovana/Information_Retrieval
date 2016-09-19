import os.path

class Fb2io:
    def __init__(self, fb2_directory):
        self.fb2_directory = fb2_directory

    def getFb2Files(self):
        fb2_files = []

        for root, dirs, files in os.walk(self.fb2_directory):
            for f in files:
                fullpath = os.path.join(root, f)
                if os.path.splitext(fullpath)[1] == '.fb2':
                    fb2_files.append(fullpath)

        return fb2_files

