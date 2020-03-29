import pandas as pd
from os import path
import gc

class DataContainer:

    _expectedExtension = '.csv'
    _df = []
    _fileName = ''
    _dataIsLoaded = False

    def __init__(self, fileName, filePath=''):
        self.loadData(fileName, filePath)

    def loadData(self, fileName, filePath):

        # Clear old data
        self.clear()

        # Check file name
        self._fileName = filePath + fileName
        if not path.isfile(self._fileName):
            raise Exception('Data file does not exist')
        if not self._fileName[-len(self._expectedExtension):] == self._expectedExtension:
            raise Exception('Unexpected file extension')

        # Load the data
        print('Loading data')
        self._df = pd.read_csv(self._fileName)
        print(self._df.head())
        self._dataIsLoaded = True
        print('Data loaded')

    def clear(self):
        # clear data if loaded
        self._fileName = ''
        if self._dataIsLoaded:
            self._df = []
            self._dataIsLoaded = False
            gc.collect()  # Force garbage collection. Safer for big df.

    # region getters
    def get_expectedExtension(self):
        return self._expectedExtension

    def get_df(self):
        return self._df

    def get_fileName(self):
        return self._fileName

    def get_dataIsLoaded(self):
        return self._dataIsLoaded
    # endregion
