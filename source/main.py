""" This file is the entry point for the data processing"""

import preprocessing as pp
import metadata as md

if __name__ == '__main__':

    # Load
    trainingData = pp.DataContainer(md.trainingFileName, md.dataPath)

    # Analysis
    trainingData.plotStats()
    dataStat = trainingData.get_dataStat()
    print("\n=========== DATA STATISTICS ===========\n"
          "Average Open ports:   ", dataStat['mean'], "\n"
          "Max Open Ports:       ", dataStat['max'], "\n"
          "Min Open Ports:       ", dataStat['min'], "\n"
          "Total time:           ", dataStat['totalTime'], "[s]\n"
          "Number of data points:", dataStat['nbData'], "\n"
          "=======================================\n")

    # Unwrap data
    trainingData.unwrapData()

    # Demean wraps
    trainingData.demeanFrames()
