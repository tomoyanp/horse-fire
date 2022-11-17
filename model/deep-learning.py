from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import tensorflow as tf
import numpy as np
import pandas
import xgboost as xgb
import lightgbm as lgb

# データセットの読み込み
data = pandas.read_csv("race_data.csv")

# カラム指定の上列抽出
specific_data = data.loc[:, ["race_id", "Nhorse_age", "Nhorse_weight", "Nweight_change", "isThird", "isSecond"]]
converted_np_array = specific_data.values

# データの正規化
# mapにばらして、race_idごとに分けていく
# つまり
# mp[race_id_no1] = [
#   [1,2,3,4,5,6],
#   [1,2,3,4,5,6],
# ]
# {202203020101:[[0.3, -3, -0.3],[0.2, 0.3, 0.3]], 202203020102:[[0.2,1,1]]}
# みたいなデータが出来る
x_mp = {} # 説明変数
y_mp = {} # 目的変数
for r in converted_np_array:
    if r[0] in x_mp:
        x_mp[r[0]].append(r[1:4].tolist())
        y_mp[r[0]].append(r[4:6].tolist())
    else:
        x_mp[r[0]] = []
        y_mp[r[0]] = []
        x_mp[r[0]].append(r[1:4].tolist())
        y_mp[r[0]].append(r[4:6].tolist())

# データの正規化
x_tmp = []
y_tmp = []
for key in x_mp.keys():
    x_tmp.append(x_mp[key])
    y_tmp.append(y_mp[key])
# ちょい怠いので一旦16頭建てのレース以外排除する
#  [[[[0.3, -3, -0.3],[0.2, 0.3, 0.3]]]]

x_data = [] # 説明変数
y_data = [] # 目的変数
for index in range(0, len(x_tmp)):
    if len(x_tmp[index]) == 16:
        x_data.append(x_tmp[index])
        y_data.append(y_tmp[index])


# 学習データとテストデータに分ける
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, random_state=0, test_size=0.3)

# 学習データを、学習用と検証用に分ける
x_train, x_eval, y_train, y_eval = train_test_split(x_train, y_train,test_size=0.2,random_state=1,
                                                    # stratify=y_train
                                                  )


# 2次元に変換する
converted_x_train = sum(x_train, [])
converted_y_train = sum(y_train, [])
converted_x_eval = sum(x_eval, [])
converted_y_eval = sum(y_eval, [])
converted_x_test = sum(x_test, [])
converted_y_test = sum(y_test, [])


# データを格納する
# 学習用
xgb_train = xgb.DMatrix(converted_x_train, label=converted_y_train)

# 検証用
xgb_eval = xgb.DMatrix(converted_x_eval, label=converted_y_eval)

# テスト用
xgb_test = xgb.DMatrix(converted_x_test, label=converted_y_test)

# クラスの比率
r_isThird, r_not_isThird = len(specific_data["isThird"] == 1), len(specific_data["isThird"] == 0)
r_all = r_isThird + r_not_isThird
print('3着以内 の割合 :',r_isThird/r_all) 
print('3着より下 の割合 :',r_not_isThird/r_all)
print(r_all)


# モデルの学習

model = lgb.LGBMClassifier() # モデルのインスタンスの作成
xgb_params = {
    'objective': 'binary:logistic',  # 2値分類問題
    'learning_rate': 0.1,            # 学習率
    'eval_metric': 'mlogloss'       # 学習用の指標
}
bst = xgb.train(xgb_params,
                    xgb_train,
                    num_boost_round=100,  # 学習ラウンド数は適当
                    )

y_pred_proba = bst.predict(xgb_test)
y_pred = np.where(y_pred_proba > 0.5, 1, 0)

acc = accuracy_score(converted_y_test, y_pred)
print(acc)