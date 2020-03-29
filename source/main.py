""" This file is the entry point for the data processing"""

import preprocessing as pp
import metadata as md

trainingData = pp.DataContainer(md.trainingFileName, md.dataPath)
