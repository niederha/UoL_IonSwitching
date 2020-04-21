import preprocessing as pp
import metadata as md
from tqdm import tqdm


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


def getMeans(df):

    # Get and sort each nb-open_channel
    openChannelList = df.open_channels.unique()
    openChannelList.sort()

    # Get each mean
    means = []
    for val in openChannelList:
        means += [df[df.open_channels.eq(val)].signal.mean()]

    return openChannelList, means


def getGetMostProbableNbOpen(signalValue, openChannelList, means):

    diffToMean = means
    for i, val in enumerate(means):
        diffToMean[i] = abs(val - signalValue)

    mostProbableValue = openChannelList[diffToMean.index(min(diffToMean))]
    return int(mostProbableValue)


if __name__ == '__main__':

    # Handle pre-processing options
    demean = True
    devariate = True
    outputFileName = 'prediction_thresholds'
    if demean:
        outputFileName += '_demeaned'
    if devariate:
        outputFileName += '_devariated'
    outputFileName += '.csv'

    # Load and preprocess training
    trainingData = pp.DataContainer(md.trainingFileName, filePath=md.dataPath, status='train')
    trainingData.unwrapData()
    if demean:
        trainingData.demeanFrames()
    if devariate:
        trainingData.devariateFrames()
    trainingData.wrapData()

    # Pre-visualisation
    trainingData.plotDataByChannels()

    # Extract threshold information
    trainingDF = trainingData.get_df()
    (openChannelList, means) = getMeans(trainingDF)
    print("Mean data:")
    print(means)

    # Load and preprocess testing data
    testData = pp.DataContainer(md.testFileName, filePath=md.dataPath, status='test')
    testData.unwrapData()
    if demean:
        testData.demeanFrames()
    if devariate:
        testData.devariateFrames()
    testData.wrapData()
    testDataStats = testData.get_dataStat()
    testDF = testData.get_df()

    # Predict values
    print("Starting predictions")
    open_channels = [0] * testDataStats['nbData']

    for i in tqdm(range(len(open_channels))):
        open_channels[i] = getGetMostProbableNbOpen(testDF.loc[i, 'signal'], openChannelList, means)

    # Export
    print("Exporting to csv...")
    testDF['open_channels'] = open_channels
    testDF.drop(columns='signal', inplace=True)
    testDF.to_csv(outputFileName, float_format='%.4f', index=False)
    print("Done")


