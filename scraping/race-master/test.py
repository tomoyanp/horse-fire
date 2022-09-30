# coding: utf-8

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
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
    return driver

f = open("race_id_list.csv", "r")
url_list = f.readlines()

write_file = open("text.html", "w", encoding="utf_8_sig")
for url in url_list:
    if url.strip() != "":
        replaced_url = url.replace("/race/", "/odds/").replace("result.html", "index.html").replace("rf=race_list", "rf=race_submenu")
        driver = getDriver()
        driver.get(replaced_url)
        time.sleep(3)
        table = driver.find_element_by_name("Ninki")
        print(table)
        # req = requests.get(replaced_url)
        # result = BeautifulSoup(req.text, "html.parser")
        # print(result)
        # write_file.write(result.text)
        # table = result.find("table", {"id": "Ninki"})
        # trs = table.findAll("tr")
        # for tr in trs:
        #     tds = tr.findAll("td")
        #     if (len(tds) > 0):
        #         name = tds[4].find("a").text
        #         odds = tds[5].find("span").text
        #         prize_odds = tds[6].find("span").text
        #         prize_odds_from = prize_odds.split("-")[0].strip()
        #         prize_odds_to = prize_odds.split("-")[1].strip()
        #         # print("%s, %s, %s, %s" % (name, odds, prize_odds_from, prize_odds_to))

