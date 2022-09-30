from keras.optimizers import Adam
import tensorflow as tf
import numpy as np


# パーセプトロンの数
N = 4  # 入力層の数
K = 20  # 隠れ層の数
M = 2  # 出力層の数

# 入力データ
# 学習データ(名前,騎手,会場など)
# 教師データ(オッズ)
trainingList = np.array([[-0.3712348946887113, -0.18229082941864605, 0.4671866368196286, 1.0191835363608703],
                         [-0.3712348946887113, 0.8280348892713083, 1.6774307432691, -0.24170990967613754]])

testingList = np.array([[-0.6879920980515413, -0.6194127660107818],
                       [-0.6358752736489328, -0.5028242358046408]])

testingList2 = np.array(
    [[-0.3712348946887113, 0.8280348892713083, -0.27240698378838185, -0.24170990967613754]])

# 3層ニューラルネットワークの構築
model = tf.keras.Sequential()
model.add(tf.keras.Input(shape=(N,)))
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
model.fit(trainingList, testingList, None, 256)

# 出力 ※ 戻り値は numpy 配列
y = model.predict(testingList2)

print('入力')
tf.print(testingList)
print('\n出力')
print(y)
