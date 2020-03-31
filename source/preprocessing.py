import pandas as pd
from os import path
import gc
import matplotlib.pyplot as plt


class DataContainer:

    _expectedExtension = '.csv'
    _df = []
    _fileName = ''
    _dataIsLoaded = False
    _dataStat = {'mean': float('nan'),
                 'histogram': {},
                 'nbData': float('nan'),
                 'totalTime': float('nan'),
                 'min': float('nan'),
                 'max': float('nan')}
    _dataStatIsLoaded = False

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

        # clear dataStats
        _dataStat = {'mean': float('nan'),
                     'histogram': {},
                     'nbData': float('nan'),
                     'totalTime': float('nan'),
                     'min': float('nan'),
                     'max': float('nan')}
        self._dataStatIsLoaded = False

    def plotStats(self):
        if not self._dataStatIsLoaded:
            self._computeDataStat()
        x = list(self._dataStat['histogram'].keys())
        y = [0] * (max(x)+1)
        for index, value in enumerate(x):
            y[index] = self._dataStat['histogram'][value]

        plt.bar(x, y)
        plt.xlabel('Number of open channels')
        plt.ylabel('Number of occurrences')
        plt.show()

    # region getters
    def get_expectedExtension(self):
        return self._expectedExtension

    def get_df(self):
        return self._df

    def get_fileName(self):
        return self._fileName

    def get_dataIsLoaded(self):
        return self._dataIsLoaded

    def get_dataStat(self):
        if not self._dataIsLoaded:
            Exception('Data should be loaded before computing stats')
        else:
            self._computeDataStat()
        return self._dataStat

    def get_dataStatIsLoaded(self):
        return self._dataStatIsLoaded

    # endregion

    # region private functions
    def _computeDataStat(self):
        if not self._dataStatIsLoaded:
            self._dataStat['mean'] = self._computeSignalMean(self._df)
            self._dataStat['histogram'] = self._computeHistogram(self._df)
            self._dataStat['nbData'] = self._computeNbRow(self._df)
            self._dataStat['totalTime'] = self._computeTotalTime(self._df)
            self._dataStat['min'] = min(list(self._dataStat['histogram'].keys()))
            self._dataStat['max'] = max(list(self._dataStat['histogram'].keys()))

    # endregion

    # region static methods
    @staticmethod
    def _computeSignalMean(df):
        return df.signal.mean()

    @staticmethod
    def _computeHistogram(df):
        return df.open_channels.value_counts().to_dict()

    @staticmethod
    def _computeNbRow(df):
        return len(df.index)

    @staticmethod
    def _computeTotalTime(df):
        return max(df.time)
    # endregion