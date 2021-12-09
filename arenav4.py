import numpy as np
import pandas as pd
import xgboost
import arenav3
from colorama import Fore, Style
import KDDataProcess as kdp


def runV4(X_test):  # , deckSelection):
    # 학습 데이터 로딩 및 학습
    df = pd.read_csv('arenaDataV4.CSV')
    X = df.drop('win', axis=1).copy()

    # 검증
    for idx, row in X.iterrows():
        for i in range(7, 12):
            if pd.isna(row[i]):  # 난일 때
                if not pd.isna(row[i+5]):  # 난이 아니면 문제
                    print("case 01 " + str(idx+2) + " " + str(i))
            else:
                if pd.isna(row[i + 5]):  # 난이 아닐 때 난이면 문제
                    print("case 02 " + str(idx+2) + " " + str(i))

    X = kdp.nanLevelAsMinus1(X)
    y = df['win'].copy()
    X_encoding = kdp.onHotEncoding(X)
    clf_xgb = xgboost.XGBClassifier(use_label_encoder=False)
    clf_xgb.fit(X_encoding, y, eval_metric='logloss')

    # 예측할 데이터 로딩
    # X_test = pd.read_csv('arenaTestV4.CSV')
    # kdp.addTestDataIntoTrainData(X_test, 'arenaDataV4.CSV')
    org_X_test = X_test

    # 변경 되기 전에 V3 만들기
    X_testV3 = kdp.transferDataToV3(X_test)

    X_test = kdp.putMoreData(kdp.nanLevelAsMinus1(X_test), 4)

    # print(X_test)

    X_test_encoding = kdp.onHotEncoding(X_test)

    # 학습 데이터 병합 및 예측
    result = X_encoding.head(0).append(X_test_encoding, sort=False)
    result = result.drop(X_test_encoding.columns.difference(X_encoding.columns), axis=1)
    result = result.replace(np.nan, '0')
    y_pred = clf_xgb.predict(result)

    y_predV3 = arenav3.runArenaV3(X_testV3)

    # print(y_predV3)
    # print(y_pred)

    count = 0
    resultString = ''

    resultString = "my_deck\t\tpaper\tv3\tv4\n------------------------------------------\n"
    # print(resultString)

    # if int(org_X_test.iloc[0]['mypaper']) > 9:
    #     rowSize = kdp.simulateSize * int(12 - org_X_test.iloc[0]['paper'] + 1)
    #
    # print(kdp.result_show_size)
    # print(rowSize)

    for idx, row in X_test.tail(kdp.result_show_size).loc[1:].iterrows():
        # v3Result = f"{Style.RESET_ALL}0"
        # v4Result = f"{Style.RESET_ALL}0"
        v3Result = "0"
        v4Result = "0"
        if y_predV3[idx] == 1:
            # v3Result = f"{Fore.RED}1"
            v3Result = "1"
        if y_pred[idx] == 1:
            # v4Result = f"{Fore.BLUE}1"
            v4Result = "1"
        # print(f"{Style.RESET_ALL}" + row['me'] + " " + str(row['paper']) + "\t\t" + v3Result+"\t"+v4Result)
        resultString += row['me'] + "\t" + str(row['paper']) + "\t" + v3Result+"\t"+v4Result + '\n'
        if idx % len(kdp.myDeck) == 0:
            resultString += '------------------------------------------\n'

        count = count + 1

    # print(resultString)
    # print(f"{Style.RESET_ALL}" + str(kdp.myDeck))
    # deck = deckSelection # input('your deck : ')
    # win = input('win : ')

    # 최종 데이터로 저장
    # kdp.addTestDataIntoTrainData(org_X_test, 'arenaDataV4.CSV', deck, win, 4)
    # kdp.addTestDataIntoTrainData(X_testV3, 'arenaDataV3.CSV', deck, win, 3)
    # print('result saved')

    return X_testV3, org_X_test, resultString

    # userInput = input('continue press enter ')
    # if int(userInput) != 1:
    #     break;
