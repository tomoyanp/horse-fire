# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time

f = open("race-data.csv", "w", encoding="utf_8_sig")
f.write("goal_order, start_number, horse_name, horse_age, weight,jockey_name,single_odds,hourse_weight,weight_change\n")

#for index in range(1, 113):
#    if (index == 1):
#        req = requests.post("https://race.netkeiba.com/race/result.html?race_id=202203020101&rf=race_list", {})
#    else:
#        req = requests.post("https://db.netkeiba.com/", {
#            "sort_key": "prize",
#            "sort_type": "desc",
#            "pid": "horse_list",
#            "list": "100",
#            "under_age": "2",
#            "over_age": "none",
#            "act": "1",
#            "page": "%s" % index
#        })

    req = requests.post("https://race.netkeiba.com/race/result.html?race_id=202203020101&rf=race_list", {})

    req.encoding = req.apparent_encoding
    result = BeautifulSoup(req.text, "html.parser")
    table = result.find("table", {"class": "RaceTable01 RaceCommon_Table ResultRefund Table_Show_Al"})
    trs = table.findAll("tr")

    for tr in trs:
        tds = tr.findAll("td")
        if (len(tds) > 0):
            goal_order = tds[0].search("Result_Num").text
            print(goal_order)

            #name_id = tds[1].find("a").get("href").split("/")[-2]
            #father = tds[6].find("a").text
            #mother = tds[7].find("a").text
            #grand_father = tds[8].find("a").text

            #f.write("%s, %s, %s, %s, %s\n" % (name, name_id, father, mother, grand_father))
    time.sleep(10)
f.close()