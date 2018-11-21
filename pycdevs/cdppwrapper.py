import subprocess, time
from subprocess import CalledProcessError

# sample cd++ command
# cd++ -m2Voronoi.ma -ooutput -t00:01:00:00 -llogs

DEFAULT_TEMP_PATH = '/tmp/'

def getRandomFilename(anExtension):
    return f'{int(time.time() * 1000)}.{anExtension}'

def getRandomFilePath(anExtension):
    return DEFAULT_TEMP_PATH + getRandomFilename(anExtension)

class SimulationNotExectutedException(Exception):
    pass

# TODO: Add some custom excepetions, which contain the STDOUT and STDERR contents
class CDPPWrapper:

    CDPP_BIN = 'cd++'

    # TODO: Add type checking to constructor
    def __init__(self, aModel, aSimulationTime):
        self.model = aModel
        self.endTime = aSimulationTime
        self.simulationProcessData = None

    def run(self):
        self.generateOutfilesPaths()
        try:
            simulationArguments = self.getArguments()
            self.simulationProcessData = subprocess.run(simulationArguments, capture_output=True, check=True)
            print(f'STDOUT:\n')
            print(self.simulationProcessData.stdout.decode('ascii'))
        except CalledProcessError as e:
            # The exception contains information about the failed simulation process
            print(f'The simulation process exeited with an errouneous return code: {e.returncode}')
    
    def getLogsPath(self):
        if not self.simulationWasExecuted():
            raise SimulationNotExectutedException()
        return self.logsFileName

    def getOutputPath(self):
        if not self.simulationWasExecuted():
            raise SimulationNotExectutedException()
        return self.outputFileName

    def simulationWasExecuted(self):
        return self.simulationProcessData is not None

    def getArguments(self):
        arguments = [self.__class__.CDPP_BIN, f'-m{self.model.getPath()}',\
            f'-o{self.outputFileName}', f'-t{self.endTime}', f'-l{self.logsFileName}']
        return arguments

    def generateOutfilesPaths(self):
        self.outputFileName = getRandomFilePath('out')
        self.logsFileName = getRandomFilePath('log')
    
class Model:
    def __init__(self, source):
        self.source = source
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