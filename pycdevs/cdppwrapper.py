import subprocess, time
from subprocess import CalledProcessError

# sample cd++ command
# cd++ -m2Voronoi.ma -ooutput -t00:01:00:00 -llogs

# sample drawlog command
# drawlog -m2Voronoi.ma -i00:00:00:100 -cvoronoiExpansion -llogs -z/tmp/altoPerro.npz

DEFAULT_TEMP_PATH = '/tmp/'

def getRandomFilename(anExtension):
    return f'{int(time.time() * 1000)}.{anExtension}'

def getRandomFilePath(anExtension):
    return DEFAULT_TEMP_PATH + getRandomFilename(anExtension)

class SimulationNotExectutedException(Exception):
    pass

class SimulationProcessFailedException(CalledProcessError):
    pass

class SimulationExecutedButFailedException(Exception):
    pass

# TODO: Find a way to use this as a general simulation exception
class SimulationException(Exception):
    def __init__(self, actualCause):
        self.cause = actualCause
    def getCause(self):
        return self.cause

class DrawlogFailedException(CalledProcessError):
    pass

# TODO: Add some custom excepetions, which contain the STDOUT and STDERR contents
class CDPPWrapper:

    CDPP_BIN = 'cd++'
    DRAWLOG_BIN = 'drawlog'
    simulationAbortedErrorMessage = 'Aborting simulation...\n'

    # TODO: Add type checking to constructor
    def __init__(self, aModel, aSimulationTime):
        self.model = aModel
        self.endTime = aSimulationTime
        self.simulationProcessData = None

    def run(self):
        self.generateOutfilesPaths()
        simulationArguments = self.getArguments()
        try:
            self.simulationProcessData = subprocess.run(simulationArguments, capture_output=True, check=True)

        except CalledProcessError as e:
            # The exception contains information about the failed simulation process
            raise SimulationProcessFailedException(e.returncode, e.cmd, e.output, e.stderr)
        if self.getSimulationStdOut().endswith(self.__class__.simulationAbortedErrorMessage):
            raise SimulationExecutedButFailedException()

    def drawlog(self, anInterval):
        if not self.simulationWasExecuted():
            raise SimulationNotExectutedException()

        self.drawlogNPPath = getRandomFilePath('npz')

        drawlogArguments = [self.__class__.DRAWLOG_BIN, f'-m{self.model.getPath()}', f'-l{self.getLogsPath()}' ,\
            f'-c{self.model.name}', f'-i{anInterval}', f'-z{self.drawlogNPPath}']

        try:
            subprocess.run(drawlogArguments, capture_output=True, check=True)
            return self.drawlogNPPath
        except CalledProcessError as e:
            # The exception contains information about the failed simulation process
            raise DrawlogFailedException(e.returncode, e.cmd, e.output, e.stderr)

        # TODO: Add check on 'Aborting simulation...' stdout last line, and throw error

    def getSimulationStdOut(self):
        return self.simulationProcessData.stdout.decode('ascii')

    def getSimulationOutput(self):
        return 'STDOUT:\n' + self.getSimulationStdOut() + '\nSTDERR:\n' + self.simulationProcessData.stderr.decode('ascii')
    
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