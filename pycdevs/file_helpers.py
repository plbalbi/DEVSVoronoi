import time

DEFAULT_TEMP_PATH = '/tmp/'


def getRandomFilename(anExtension):
    return "{}.{}".format(int(time.time() * 1000), anExtension)


def getRandomFilePath(anExtension):
    return DEFAULT_TEMP_PATH + getRandomFilename(anExtension)
