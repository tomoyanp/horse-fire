# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time

raceData = open("race_date.csv", "w", encoding="utf_8_sig")
raceData.write("race_id,goal_order, start_number, horse_name, horse_age, weight,jockey_id,single_odds,hourse_weight,weight_change\n")

index = 0
urlList = open('race_id_list.csv', 'r')

for url in urlList:
    print("対象URL :"+url) 
    req = requests.post(url,
    {"pid": "horse_list"}
    )

    req.encoding = req.apparent_encoding
    result = BeautifulSoup(req.text, "html.parser")
    table = result.find("table", {"id": "All_Result_Table"})
    trs = table.findAll("tr")
    
    #レースIDはURLから取得
    race_id = url.replace('https://race.netkeiba.com/race/result.html?race_id=','').split('&')[0]
    for tr in trs:
        tds = tr.findAll("td")
        if (len(tds) > 0):
            goal_order = tds[0].text.strip()
            #中止もしくは取消と数字の順位が入っていない場合、登録データから除外
            if goal_order.isdecimal():
                start_number = tds[2].text.strip()
                horse_name = tds[3].text.strip()
                horse_age = tds[4].text.strip()[1:]
                weight = tds[5].text.strip()
                jockey_id = tds[6].find('a').get('href').split("/")[-2]
                single_odds = tds[10].text.strip()
                hourse_weight = tds[14].text.split("(")[0].strip()
                weight_change = tds[14].text.split("(")[1].strip().rstrip(")")
                raceData.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (race_id,goal_order, start_number, horse_name, horse_age, weight,jockey_id,single_odds,hourse_weight,weight_change) )
    time.sleep(5)

raceData.close()
urlList.close()
