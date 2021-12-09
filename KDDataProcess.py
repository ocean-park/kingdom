import numpy as np
import pandas as pd

simulateSize = 4
myDeck = ['용바블퓨정', '홀샤바펌퓨', '홀바펌목퓨', '홀바서목파']  # , '홀딸샤바퓨', '홀딸바펌퓨'] #, '홀샤바펌퓨', '홀바감펌퓨'
myPower = ['680550', '691809', '591700', '644100'] #689994
enDeck = ['홀', '샤', '바', '펌', '퓨', '목', '딸', '파', '서', '들', '마', '블', '오', '민', '락', '떼', '즐', '샴', '허', '정', '뱀', '달', '감']
enDeckDefaultLevel = [2, 5, 2, 4, 2, 3, 5, 4, 1, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5]
result_show_size = len(myDeck) * simulateSize


def putMoreData(inputData, version):
    inputLen = len(inputData)

    for i in range(0, simulateSize):
        for (deck, power) in zip(myDeck, myPower):
            if inputData['paper'].iat[0] + i > 12:
                break
            inputData = inputData.append(inputData.iloc[0], ignore_index=True)
            inputData['me'].iat[-1] = deck
            if version == 4:
                inputData['mypower'].iat[-1] = power
            inputData['paper'].iat[-1] = inputData['paper'].iat[0] + i

    # print(inputData)
    return inputData


def nanLevelAsMinus1(orgData):
    orgData = orgData.replace(
        {'l1': {np.nan: -1}, 'l2': {np.nan: -1}, 'l3': {np.nan: -1}, 'l4': {np.nan: -1}, 'l5': {np.nan: -1}})
    return orgData


def onHotEncoding(dataTobeEncoded):
    return pd.get_dummies(dataTobeEncoded, columns=['me', 'c1', 'c2', 'c3', 'c4', 'c5'])


def removeLastEmpty(fileName):
    file_data = open(fileName, 'rb').read()
    open(fileName, 'wb').write(file_data[:-2])


def transferDataToV3(inputData):
    X_test_v3 = pd.read_csv('arenaTest.CSV')

    for index, val in X_test_v3.iloc[len(X_test_v3) - 1].iteritems():
        X_test_v3[index] = inputData[index].iloc[len(inputData) - 1]

    # X_test_v3.to_csv('arenaTest.CSV', index = False)
    # removeLastEmpty('arenaTest.CSV')

    return X_test_v3


def addTestDataIntoTrainData(testData, fileName, deck, win, version):
    testData['me'] = myDeck[int(deck)]
    if version == 4:
        testData['mypower'] = myPower[int(deck)]
    testData['win'] = int(win)

    # print(testData)

    trainedPlusTest = pd.read_csv(fileName)
    trainedPlusTest = trainedPlusTest.append(testData, ignore_index=True, sort=False)
    trainedPlusTest = trainedPlusTest.astype(
        {'l1': 'Int64', 'l2': 'Int64', 'l3': 'Int64', 'l4': 'Int64', 'l5': 'Int64', 'win': 'Int64'})

    trainedPlusTest.to_csv(fileName, index=False)
    trainedPlusTest.to_csv(fileName, index=False)
    removeLastEmpty(fileName)
    # fileRead = open(fileName)
    # fileRead.flush()
