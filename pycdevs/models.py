from .file_helpers import getRandomFilename, getRandomFilePath
import numpy as np


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


class CellValues:
    def __init__(self, cell_values, default_cell_value):
        # Initialize random filename for values file
        self.path = getRandomFilePath("val")
        self.default = default_cell_value

        if not isinstance(cell_values, np.ndarray):
            raise Exception('cell_values should be NumPy ndArray')

        if len(cell_values.shape) != 2:
            raise Exception('Only 2-dimensional models are accepted so far')

        self.values = cell_values

    def get_dimension(self):
        return f'({self.values.shape[0]},{self.values.shape[1]})'

    def write_to_file(self) -> str:
        """Writes the given values to a initialCellValues file, returning the path to it."""
        with open(self.path, "w") as values_file:
            for i in range(self.values.shape[0]):
                for j in range(self.values.shape[1]):
                    current_cell_value = self.values[i, j]
                    if self.values[i, j] != self.default:
                        values_file.write(f'({i},{j})={current_cell_value}\n')

        return self.path





