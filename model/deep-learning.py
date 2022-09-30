from keras.optimizers import Adam
import tensorflow as tf
# パーセプトロンの数
N = 3  # 入力層の数
K = 5  # 隠れ層の数
M = 2  # 出力層の数

# 入力データ
# 学習データ(名前,騎手,会場など)
training = tf.constant([[1, 2, 3], [4, 5, 6]], dtype=tf.float32)
# 教師データ(オッズ)
testing = tf.constant([[0.8], [0.2]], dtype=tf.float32)

# 3層ニューラルネットワークの構築
model = tf.keras.Sequential()
model.add(tf.keras.Input(shape=(N,)))
model.add(tf.keras.layers.Dense(K, activation='tanh'))
model.add(tf.keras.layers.Dense(M, activation='softmax'))

#  fitするためにコンパイルする
opt = Adam(training, testing)
model.compile(
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# モデルの概要表示
model.summary()

# 固定回数（データセットの反復）の試行でモデルを学習
model.fit(training, testing)

# 出力 ※ 戻り値は numpy 配列
y = model.predict(training)

print('入力')
tf.print(testing)
print('\n出力')
print(y)
