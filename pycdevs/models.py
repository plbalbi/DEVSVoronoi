from .file_helpers import getRandomFilename, getRandomFilePath

class Model:
    def __init__(self, source, modelName):
        self.source = source
        self.name = modelName
        self.path = None
    
    # Lazily write model file
    def getPath(self):
        if self.path is None:
            self.doGetPath()
        return self.path

    def doGetPath(self):
        self.path = getRandomFilePath('ma')
        with open(self.path, 'w') as modelFile:
            modelFile.write(self.source)