""" This file contains metadata, constants and paths to be used during data analysis """
import os

rootDir = os.getcwd()
dataPath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/..")  # ugly but robust
dataPath = dataPath + "/data/"
trainingFileName = 'train.csv'
testFileName = 'test.csv'
