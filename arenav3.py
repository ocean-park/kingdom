import numpy as np
import pandas as pd
import xgboost
import KDDataProcess as kdp


def runArenaV3(X_testV3):
    # 학습 데이터 로딩 및 학습
    df = pd.read_csv('arenaDataV3.CSV')
    X = df.drop('win', axis=1).copy()
    # 검증
    for idx, row in X.iterrows():
        for i in range(1, 6):
            # print(idx)
            # print(row[i])
            # print(row[i+5])
            if pd.isna(row[i]):  # 난일 때
                if not pd.isna(row[i+5]):  # 난이 아니면 문제
                    print("case 01 " + str(idx+2) + " " + str(i))
                    # raise NotImplementedError
            else:
                if pd.isna(row[i + 5]):  # 난이 아닐 때 난이면 문제
                    print("case 02 " + str(idx+2) + " " + str(i))
                    # raise NotImplementedError

    X = kdp.nanLevelAsMinus1(X)
    y = df['win'].copy()
    X_encoding = kdp.onHotEncoding(X)
    clf_xgb = xgboost.XGBClassifier(use_label_encoder=False)
    clf_xgb.fit(X_encoding, y, eval_metric='logloss')

    # 예측할 데이터 로딩
    # X_test = pd.read_csv('arenaTest.CSV')
    X_test = kdp.putMoreData(kdp.nanLevelAsMinus1(X_testV3), 3)
    X_test_encoding = kdp.onHotEncoding(X_test)

    # 학습 데이터 병합 및 예측
    result = X_encoding.head(0).append(X_test_encoding, sort=False)
    result = result.drop(X_test_encoding.columns.difference(X_encoding.columns), axis=1)
    # result = result.tail(result_show_size)
    result = result.replace(np.nan, '0')
    y_pred = clf_xgb.predict(result)

    # count = 0
    # print(y_pred)
    # print("my_deck  paper\twin ---- v3")
    # for idx, row in X_test.tail(result_show_size).iloc[1:].iterrows():
    #     if y_pred[idx] == 1:
    #         print('\033[31m' + row['me'] + " " + str(row['paper']) + "\t\t" + str(y_pred[idx]) + '\033[0m')
    #     else:
    #         print(row['me'] + " " + str(row['paper']) + "\t\t" + str(y_pred[idx]))
    #     count = count + 1

    # print(y_pred)
    return y_pred
    # print(result.tail(result_show_size))
    # X_encoding.to_csv('./sampleX.CSV', sep=',', na_rep='NaN')
    # X_test.to_csv('./samplePred.CSV', sep=',', na_rep='NaN')
    # X_test_encoding.to_csv('./samplePredOHE.CSV', sep=',', na_rep='NaN')
    # result.to_csv('./result.CSV', sep=',', na_rep='NaN')
