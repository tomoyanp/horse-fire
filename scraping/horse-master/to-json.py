# coding: utf-8

csv_file = open('horse-master.csv')
data = csv_file.read().split("\n")

horse_list = []
bread_dict = {}
for r in data:
    column = r.split(",")
    if len(column) > 1:
        bread_dict[column[0].strip()] = {}
        bread_dict[column[0].strip()]["father"] = column[2]
        bread_dict[column[0].strip()]["mother"] = column[3]
        bread_dict[column[0].strip()]["grand_father"] = column[4]
        horse_list.append(column[0].strip())
        horse_list.append(column[2].strip())
        horse_list.append(column[3].strip())
        horse_list.append(column[4].strip())


horse_set = set(horse_list)
horse_unique_list = list(horse_set)

horse_dict = {}
for i in range(0, len(horse_unique_list)):
    horse_dict[horse_unique_list[i]] = i

bread_json = open("bread.json", mode="w")
horse_json = open("horse.json", mode="w")

import json

json.dump(bread_dict, bread_json, indent=2, ensure_ascii=False)
json.dump(horse_dict, horse_json, indent=2, ensure_ascii=False)

horse_json.close()
bread_json.close()
