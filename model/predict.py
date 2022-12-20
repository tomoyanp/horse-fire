# coding: utf-8
import os
import sys
import lightgbm as lgb
import pandas
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scraping.race_master import race_data
import json

predict_url = "https://race.netkeiba.com/race/result.html?race_id=202205050812&rf=race_list"

bread_map = json.load(open("../scraping/horse-master/bread.json"))
horse_map = json.load(open("../scraping/horse-master/horse.json"))
driver = race_data.getDriver()
horse_list = race_data.createHorseList(predict_url, driver, horse_map, bread_map)

# めんどいから一度CSVに出そう。。。
field_name = ["race_id", "goal_order", "start_number", "horse_name", "horse_age", "weight", "jockey_id", "single_odds", "horse_weight", "weight_change", "multi_odds", "is_third", "is_second", "weather", "ground_condition", "horse_id", "father_id", "mother_id", "grand_father_id"]
#2行目以降は配列を出力するのでcsv.write利用する
f = open("predict.csv", "w", encoding="utf_8_sig")
raceWriter = csv.DictWriter(f, fieldnames=field_name)
raceWriter.writeheader()
raceWriter.writerows(horse_list)
f.close()

data = pandas.read_csv("predict.csv")
d = data.loc[:, ["start_number", "horse_age", "weight", "single_odds", "horse_weight", "weight_change", "multi_odds", "weather", "ground_condition", "horse_id", "father_id", "mother_id", "grand_father_id"]]

model = lgb.Booster(model_file="model.txt")
y = model.predict(d)

for res in y:
    print(res)

