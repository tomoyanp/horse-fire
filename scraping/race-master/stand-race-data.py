import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

#Pandasに全行読み込み&カラム指定
raceData = pd.read_csv("race_data.csv").values.tolist()
dfRaceData = pd.DataFrame(raceData,columns=['race_id','goal_order','start_number','horse_name','horse_age','weight','jockey_id','single_odds','hourse_weight','weight_change','multi_odds'])

#標準化対象カラム指定
scalingColumns = ['horse_age','weight','single_odds','hourse_weight','weight_change','multi_odds'] 
sc = StandardScaler().fit(dfRaceData[scalingColumns])

#標準化されたカラムとされていないカラムを統合してDataraFrameを作成
scaledRaceData = pd.DataFrame(sc.transform(dfRaceData[scalingColumns]), columns=scalingColumns, index=dfRaceData.index)
dfRaceData.update(scaledRaceData)

#標準化されたファイルをCSVに出力
dfRaceData.to_csv('std_race_data.csv')
