import preprocessing as pp
import metadata as md

def visualiseThesholdData():
    trainingData = pp.DataContainer(md.trainingFileName, md.dataPath)

    # plot raw data
    trainingData.plotDataByChannels()

    # plot demeaned data
    trainingData.unwrapData()
    trainingData.demeanFrames()
    trainingData.wrapData()
    trainingData.plotDataByChannels()

    # plot normalized data
    trainingData.devariateFrames()
    trainingData.wrapData()
    trainingData.plotDataByChannels()

if __name__ == '__main__':

    visualiseThesholdData()