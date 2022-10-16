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
        # print(pageSource)
        # req = requests.get(replaced_url)
        result = BeautifulSoup(pageSource, "html.parser")
        # print(result)
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

if __name__ == '__main__':

    #レース情報を取得するレースID
    urlList = open('race_id_list.csv', 'r')

    #レース情報を出力するファイル
    raceData = open("race_data.csv", "w", encoding="utf_8_sig")
    raceData.write("race_id,goal_order, start_number, horse_name, horse_age, weight,jockey_id,single_odds,hourse_weight,weight_chang,multiOdds,isThird,isSecond,Nhorse_age,Nhorse_weight,Nsingle_odds,Nhourse_weight,Nweight_change,Nmulti_odds\n")
    #2行目以降は配列を出力するのでcsv.write利用する
    raceWriter = csv.writer(raceData)

    #Chrome Driver
    googleDriver = getDriver()

    for url in urlList:
        print("対象URL:"+url)

        #オッズ情報を取得
        odds_obj = getOdds(url,googleDriver)

        #オッズが取れない場合、対象レースはスキップ
        if odds_obj is None:
            continue

        #レース情報を取得
        req = requests.post(url,{"pid": "horse_list"})       
        req.encoding = req.apparent_encoding
        result = BeautifulSoup(req.text, "html.parser")
        table = result.find("table", {"id": "All_Result_Table"})
        trs = table.findAll("tr")
    
        horseList = []
        for tr in trs:
            tds = tr.findAll("td")
            if (len(tds) > 0):
                #着順に中止もしくは取消と数字の順位が入っている場合、登録データから除外
                if tds[0].text.strip().isdecimal():
                    horse = []
                    horse.append(url.replace('https://race.netkeiba.com/race/result.html?race_id=','').split('&')[0]) #race_id(URLから取得)
                    horse.append(tds[0].text.strip())   #goal_order
                    horse.append(tds[2].text.strip())   #start_number
                    horse.append(tds[3].text.strip())   #horse_name
                    horse.append(float(tds[4].text.strip()[1:]))    #horse_age(標準化対象)
                    horse.append(float(tds[5].text.strip()))        #weight(標準化対象)
                    horse.append(tds[6].find('a').get('href').split("/")[-2])   #jockey_id
                    horse.append(float(tds[10].text.strip()))                   #single_odds(標準化対象)
                    horse.append(float(tds[14].text.split("(")[0].strip()))     #hourse_weight(標準化対象)
                    horse.append(float(tds[14].text.split("(")[1].strip().rstrip(")"))) #weight_change(標準化対象)
                    horse.append(float(odds_obj[tds[3].text.strip()]))                  #multi_odds (HorsenameがKey)(標準化対象)
                    if tds[0].text.strip() in ['1','2','3']:        #isThird
                        horse.append('1')
                    else:
                        horse.append('0')
                    if tds[0].text.strip() in ['1','2']:            #isSecond
                        horse.append('1')
                    else:
                        horse.append('0')
                    horseList.append(horse)
        #レースID単位で標準化&カラム追加
        normalizedHorseList= normalize(horseList)
        try:
            raceWriter.writerows(normalizedHorseList)
#           raceData.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (race_id,goal_order, start_number, horse_name, horse_age, weight,jockey_id,single_odds,hourse_weight,weight_change,) )
        except Exception as e:
            print(e)
        time.sleep(2)

    #Chrome Driverは絶対殺すマン
    googleDriver.quit()
    raceData.close()
    urlList.close()
    