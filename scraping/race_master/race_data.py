# coding: utf-8

import numpy as np
import csv

import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json



def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
    return driver

def getOdds(url,googleDriver):
    replaced_url = url.replace("/race/", "/odds/").replace("result.html", "index.html").replace("rf=race_list", "rf=race_submenu")
    googleDriver.get(replaced_url)

    # time.sleep(3)
    # table = driver.find_element_by_name("Ninki")
    isExist = WebDriverWait(googleDriver, 3).until(EC.visibility_of_element_located((By.ID, 'Ninki')))
    if isExist:
        pageSource = googleDriver.page_source
        # req = requests.get(replaced_url)
        result = BeautifulSoup(pageSource, "html.parser")
        # write_file.write(result.text)
        table = result.find("table", {"id": "Ninki"})
        trs = table.findAll("tr")
        rtn_obj = {}
        for tr in trs:
            tds = tr.findAll("td")
            if (len(tds) > 0):
                try:
                    name = tds[4].find("a").text
                    prize_odds = tds[6].find("span").text
                    prize_odds_from = prize_odds.split("-")[0].strip()
                    prize_odds_to = prize_odds.split("-")[1].strip()
                    rtn_obj[name] = (float(prize_odds_from) + float(prize_odds_to)) / 2
                except Exception as e:
                    #出走中止でオッズが取れない馬がいる場合に発生
                    print(e)
                    return None
        return rtn_obj

def normalize(horseList):

    npArry = np.array(horseList,dtype='object')
    #標準化対象：horse_age,single_odds,hourse_weight,weight_change,multi_odds
    for y in 4,5,7,8,9,10:
        #標準偏差が1の場合はとりあえず1で除算（全頭同じ年齢の場合に発生する：そもそも年齢は標準化しなくてもいいかも）
        if np.std(npArry[:,y]) == 0:
            std = npArry[:,y] - np.mean(npArry[:,y])
        else:
            std = (npArry[:,y] - np.mean(npArry[:,y]) ) / np.std(npArry[:,y])
        #標準化された1次元配列を追加する
        npArry = np.column_stack([npArry,std])
    return npArry

def decideWeather(text):
    if re.search("天候:晴", text):
        return 0 
    elif re.search("天候:曇", text):
        return 1 
    elif re.search("天候:雨", text):
        return 2
    elif re.search("天候:雪", text):
        return 3

    return ""

def decideGround(text):
    if re.search("馬場:良", text):
        return 0
    elif re.search("馬場:稍", text):
        return 1
    elif re.search("馬場:重", text):
        return 2

    return ""

def createHorseList(url, googleDriver, horse_map, bread_map):
    #オッズ情報を取得
    odds_obj = getOdds(url,googleDriver)

    #オッズが取れない場合、対象レースはスキップ
    if odds_obj is None:
        return None 


    #レース情報を取得
    req = requests.post(url,{"pid": "horse_list"})       
    req.encoding = req.apparent_encoding
    result = BeautifulSoup(req.text, "html.parser")

    race_data = result.find("div", class_="RaceData01")
    weather = decideWeather(race_data.text)
    ground_condition = decideGround(race_data.text)
    
    table = result.find("table", {"id": "All_Result_Table"})
    trs = table.findAll("tr")

    
    horseList = []
    for tr in trs:
        tds = tr.findAll("td")
        if (len(tds) > 0):
            #着順に中止もしくは取消と数字の順位が入っている場合、登録データから除外
            if tds[0].text.strip().isdecimal():
                horse = {} 
                horse["race_id"] = url.replace('https://race.netkeiba.com/race/result.html?race_id=','').split('&')[0] #race_id(URLから取得)
                horse["goal_order"] = tds[0].text.strip()   #goal_order
                horse["start_number"] = tds[2].text.strip()   #start_number
                horse["horse_name"] = tds[3].text.strip()   #horse_name
                horse_name = tds[3].text.strip()
                bread_data = bread_map[horse_name]
                horse_id = horse_map[horse_name]

                father_id = horse_map[bread_data["father"].strip()]
                mother_id = horse_map[bread_data["mother"].strip()]
                grand_father_id = horse_map[bread_data["grand_father"].strip()]

                horse["horse_age"] = float(tds[4].text.strip()[1:])    #horse_age(標準化対象)
                horse["weight"] = float(tds[5].text.strip())        #weight(標準化対象)
                horse["jockey_id"] = tds[6].find('a').get('href').split("/")[-2]   #jockey_id
                horse["single_odds"] = float(tds[10].text.strip())                   #single_odds(標準化対象)
                horse["horse_weight"] = float(tds[14].text.split("(")[0].strip())     #hourse_weight(標準化対象)

                # 外国馬だと馬体重の増減が乗ってなかったりするので
                splited_weight = tds[14].text.split("(")
                if (len(splited_weight) > 1):
                    horse["weight_change"] = float(splited_weight[1].strip().rstrip(")")) #weight_change(標準化対象)
                else:
                    horse["weight_change"] = 0

                horse["multi_odds"] = float(odds_obj[tds[3].text.strip()])                  #multi_odds (HorsenameがKey)(標準化対象)
                if tds[0].text.strip() in ['1','2','3']:        #isThird
                    horse["is_third"] = "1"
                else:
                    horse["is_third"] = "0"
                if tds[0].text.strip() in ['1','2']:            #isSecond
                    horse["is_second"] = "1"
                else:
                    horse["is_second"] = "0"
                horse["weather"] = weather # 天気
                horse["ground_condition"] = ground_condition # 馬場状態
                horse["horse_id"] = horse_id # 馬ID
                horse["father_id"] = father_id # 父
                horse["mother_id"] = mother_id # 母
                horse["grand_father_id"] = grand_father_id # 母父
                horseList.append(horse)

    
    return horseList



if __name__ == '__main__':
    # 馬データ
    bread_map = json.load(open("../horse-master/bread.json"))
    horse_map = json.load(open("../horse-master/horse.json"))
    #Chrome Driver
    googleDriver = getDriver()

    #レース情報を取得するレースID
    urlList = open('race_id_list.csv', 'r')

    #レース情報を出力するファイル
    raceData = open("race_data.csv", "w", encoding="utf_8_sig")
    field_name = ["race_id", "goal_order", "start_number", "horse_name", "horse_age", "weight", "jockey_id", "single_odds", "horse_weight", "weight_change", "multi_odds", "is_third", "is_second", "weather", "ground_condition", "horse_id", "father_id", "mother_id", "grand_father_id"]
    #2行目以降は配列を出力するのでcsv.write利用する
    raceWriter = csv.DictWriter(raceData, fieldnames=field_name)
    raceWriter.writeheader()

    for row in urlList:
        try:
            url = row.split(",")[0]
            print("対象URL:"+url)
            horseList = createHorseList(url, googleDriver, horse_map, bread_map)

            if horseList is None:
                continue
            raceWriter.writerows(horseList)
        except Exception as e:
            print(e)
        time.sleep(2)
    #Chrome Driverは絶対殺すマン
    googleDriver.quit()
    raceData.close()
    urlList.close()
    
