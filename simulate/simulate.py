# coding: utf-8
import pandas

data = pandas.read_csv("../model/race_data.csv")
df = data.loc[:, ["race_id", "goal_order", " start_number", "single_odds", "multiOdds"]]

# 引数にrace_idと馬三頭を渡すと、3連複を買ったものとして結果を返してくれる
# 三連複オッズは計算が怠いので、疑似的に複勝1*複勝2*複勝3とする
# 掛け金はとりあえずシンプルに1000円とする
# 結果は下記を配列にしたもの
# [raceID, 選んだ3頭, 実際の3頭, 払い戻し額]
amount = 1000
def simulate(race_id, expect):
    race_data = df[df.race_id==race_id]
    actual = []
    first = race_data[race_data.goal_order == 1]
    second = race_data[race_data.goal_order == 2]
    third = race_data[race_data.goal_order == 3]
    actual.append(first[" start_number"].tolist()[0])
    actual.append(second[" start_number"].tolist()[0])
    actual.append(third[" start_number"].tolist()[0])

    sorted_actual = sorted(actual)
    sorted_expect = sorted(expect)

    result = [race_id]
    result.extend(expect)
    result.extend(actual)
    if sorted_expect == sorted_actual:
        value = first["multiOdds"].tolist()[0] * second["multiOdds"].tolist()[0] * third["multiOdds"].tolist()[0] * amount
        result.append(value)
    else:
        result.append(-1 * amount)

    return result


