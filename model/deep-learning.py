# coding: utf-8 
from keras.optimizers import Adam
import tensorflow as tf
import numpy as np
import pandas


# パーセプトロンの数
N = 4  # 入力層の数
K = 20  # 隠れ層の数
M = 2  # 出力層の数


data = pandas.read_csv("std_race_data.csv")

# カラム指定の上列抽出
# この時点では
# rade_id, horse_age, weight...の行列
training_data = data.loc[:, ["race_id", "horse_age",
                             "weight", "hourse_weight", "weight_change", "single_odds", "multi_odds"]]
np_array = training_data.values

# mapにばらして、race_idごとに分けていく
# つまり
# mp[race_id_no1] = [
#   [1,2,3,4,5,6],
#   [1,2,3,4,5,6],
# ]
# みたいなデータが出来る
# ついでに正解データも作る
mp = {}
mp_answer = {}
for r in np_array:
    if r[0] in mp:
        mp[r[0]].append(r[1:5].tolist())
        mp_answer[r[0]].append(r[5:7].tolist())
    else:
        mp[r[0]] = []
        mp_answer[r[0]] = []
        mp[r[0]].append(r[1:5].tolist())
        print(r)
        mp_answer[r[0]].append(r[5:7].tolist())

tmp_data = []
tmp_answer = []
for key in mp.keys():
    tmp_data.append(mp[key])
    tmp_answer.append(mp_answer[key])

# ちょい怠いので一旦16頭建てのレース以外排除する
training_data = []
answer_data = []
for index in range(0, len(tmp_data)):
    if len(tmp_data[index]) == 16:
        training_data.append(tmp_data[index])
        answer_data.append(tmp_answer[index])

trainingList = training_data
answerList = answer_data
# d = pandas.DataFrame(training_data)
# a = pandas.DataFrame(answer_data)
# trainingList = d.values
# answerList = a.values

# 入力データ

# 学習データ(名前,騎手,会場など)
# trainingList = np.array([
#     [
#         [-0.6879920980515413, -0.6194127660107818, 0.1234, -0.1234],
#         [-0.6358752736489328, -0.5028242358046408, 0.1234, -0.1234]
#     ],
#     [
#         [-0.6879920980515413, -0.6194127660107818, 0.1234, -0.1234],
#         [-0.6358752736489328, -0.5028242358046408, 0.1234, -0.1234]
#     ]
# ])

# 教師データ(単勝オッズ、複勝オッズ)
# answerList = np.array([
#     [
#         [0.9, 0.3],
#         [0.3, 0.1]
#     ],
#     [
#         [0.9, 0.3],
#         [0.3, 0.1]
#     ]
# ])

# テストデータ
# データ構造は学習データと同じ。学習済モデルの精度を上げるために必要
# testingList = np.array([
#     [
#         [-0.6879920980515413, -0.6194127660107818, 0.1234, -0.1234],
#         [-0.6358752736489328, -0.5028242358046408, 0.1234, -0.1234]
#     ],
#     [
#         [-0.6879920980515413, -0.6194127660107818, 0.1234, -0.1234],
#         [-0.6358752736489328, -0.5028242358046408, 0.1234, -0.1234]
#     ]
# ])


# 3層ニューラルネットワークの構築
model = tf.keras.Sequential()
model.add(tf.keras.Input(shape=(16, 4)))
model.add(tf.keras.layers.Dense(K, activation='tanh'))
model.add(tf.keras.layers.Dense(M, activation='softmax'))

#  fitするためにコンパイルする
model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
)

# モデルの概要表示
model.summary()

# 固定回数（データセットの反復）の試行でモデルを学習
model.fit(trainingList, answerList, None, 256)

# 出力 ※ 戻り値は numpy 配列
# To Endo ここは任せた
# y = model.predict(testingList)




