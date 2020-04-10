""" This file contains metadata, constants and paths to be used during data analysis """
import os

# Path management
rootDir = os.getcwd()
dataPath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/..")  # ugly but robust
dataPath = dataPath + "/data/"
trainingFileName = 'train.csv'
testFileName = 'test.csv'

# Data formatting/splitting
acquisitionRate = 10000     # [Hz]
continuousSampleTime = 50   # [S]
nbContinuousSamples = continuousSampleTime * acquisitionRate  # [-]


