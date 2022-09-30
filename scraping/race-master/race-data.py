# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

raceData = open("race_date.csv", "w", encoding="utf_8_sig")
raceData.write("race_id,goal_order, start_number, horse_name, horse_age, weight,jockey_id,single_odds,hourse_weight,weight_change\n")

index = 0
urlList = open('race_id_list.csv', 'r')

def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
    return driver

def getOdds(url):
    replaced_url = url.replace("/race/", "/odds/").replace("result.html", "index.html").replace("rf=race_list", "rf=race_submenu")
    driver = getDriver()
    driver.get(replaced_url)
    time.sleep(3)
    # table = driver.find_element_by_name("Ninki")
    isExist = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, 'Ninki')))
    if isExist:
        pageSource = driver.page_source
        print(pageSource)
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
                name = tds[4].find("a").text
                prize_odds = tds[6].find("span").text
                prize_odds_from = prize_odds.split("-")[0].strip()
                prize_odds_to = prize_odds.split("-")[1].strip()
                rtn_obj[name] = (prize_odds_from + prize_odds_to) / 2
                return rtn_obj


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
    odds_obj = getOdds(url)
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
                raceData.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (race_id,goal_order, start_number, horse_name, horse_age, weight,jockey_id,single_odds,hourse_weight,weight_change,odds_obj[horse_name]) )
    time.sleep(5)

raceData.close()
urlList.close()
