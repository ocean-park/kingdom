import numpy as np
import pandas as pd
import xgboost


def putMoreData(inputData):
    myDeck = ['용바블퓨정', '홀라바퓨정', '홀딸샤바퓨', '홀샤바펌퓨']

    inputLen = len(inputData)

    for i in range(0, 3):
        for deck in myDeck:
            inputData = inputData.append(inputData.iloc[inputLen - 1], ignore_index=True)
            inputData['me'].iat[-1] = deck
            inputData['paper'].iat[-1] = inputData['paper'].iat[-1] + i

    return inputData


result_show_size = 12

# 학습 데이터 로딩
df = pd.read_csv('arenaDataV3.CSV')
X = df.drop('win', axis=1).copy()
# cols = ['l1', 'l2', 'l3', 'l4', 'l5']
X = X.replace({'l1': {np.nan: -1}, 'l2': {np.nan: -1}, 'l3': {np.nan: -1}, 'l4': {np.nan: -1}, 'l5': {np.nan: -1}})
# df["column1"].replace({"a": "x", "b": "y"}, inplace=True)

y = df['win'].copy()
X_encoding = pd.get_dummies(X, columns=['me', 'c1', 'c2', 'c3', 'c4', 'c5'])
# print(X_encoding.head())

clf_xgb = xgboost.XGBClassifier(use_label_encoder=False)
clf_xgb.fit(X_encoding, y, eval_metric='logloss')

# 예측할 데이터 로딩
X_test = pd.read_csv('arenaTest.CSV')
X_test = X_test.replace({'l1': {np.nan: -1}, 'l2': {np.nan: -1}, 'l3': {np.nan: -1}, 'l4': {np.nan: -1}, 'l5': {np.nan: -1}})
X_test = putMoreData(X_test)
X_test_encoding = pd.get_dummies(X_test, columns=['me', 'c1', 'c2', 'c3', 'c4', 'c5'])

# 학습 데이터 병합
result = X_encoding.head(1).append(X_test_encoding, sort=False)
result = result.drop(X_test_encoding.columns.difference(X_encoding.columns), axis=1)

result = result.tail(result_show_size)
result = result.replace(np.nan, '0')

y_pred = clf_xgb.predict(result)

count = 0
# print(y_pred)
for ending_price in X_test.tail(result_show_size)['me'].values:
    if y_pred[count-result_show_size] == 1:
        print('\033[31m' + ending_price + " " + str(y_pred[count - result_show_size]) + '\033[0m')
    else:
        print(ending_price + " " + str(y_pred[count - result_show_size]))
    count = count + 1

# print(result.tail(result_show_size))
# X_encoding.to_csv('./sampleX.CSV', sep=',', na_rep='NaN')
# X_test.to_csv('./samplePred.CSV', sep=',', na_rep='NaN')
# X_test_encoding.to_csv('./samplePredOHE.CSV', sep=',', na_rep='NaN')
# result.to_csv('./result.CSV', sep=',', na_rep='NaN')
