import preprocessing as pp
import metadata as md
import random
from tqdm import tqdm
import time

def buildAgregatedPrior(histogram):
    agregatedPior = [0] * (len(histogram) + 1)
    normalHisto = [elem/sum(histogram) for elem in histogram]
    for i in range(len(normalHisto)-1):
        agregatedPior[i+1] = agregatedPior[i] + normalHisto[i]
    agregatedPior[-1] = 1
    return agregatedPior


def priorBasedRandomPrediciton(agragatedPrior):
    rndNum = random.uniform(0, 1)
    for i in range(len(agragatedPrior)-1):
        if agragatedPrior[i] <= rndNum < agragatedPrior[i+1]:
            break
    return i


if __name__ == '__main__':

    # Get training data and compute stats
    trainingData = pp.DataContainer(md.trainingFileName, filePath=md.dataPath, status='train')
    trainingData.plotStats()
    trainingDataStat = trainingData.get_dataStat()

    # Get test data
    testData = pp.DataContainer(md.testFileName, filePath=md.dataPath, status='test')
    testDf = testData.get_df()
    testDataStats = testData.get_dataStat()

    # Compute prior
    histogram = list(trainingDataStat['histogram'].values())
    agragatedPrior = buildAgregatedPrior(histogram)

    # Make a random prediction
    print("\nMaking a random prediction")
    time.sleep(1)  # Just not to fuck up the display
    open_channels = [0] * testDataStats['nbData']
    for i in tqdm(range(len(open_channels))):
        predictionIndex = priorBasedRandomPrediciton(agragatedPrior)
        open_channels[i] = list(trainingDataStat['histogram'].keys())[predictionIndex]  # a bit twisted but ok

    # Export
    print("Exporting to csv...")
    testDf['open_channels'] = open_channels
    testDf.drop(columns='signal', inplace=True)
    testDf.to_csv('random_prediction.csv', float_format='%.4f', index=False)
    print("Done")
