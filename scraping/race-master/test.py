# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time

f = open("race_id_list.csv", "r")
url_list = f.readlines()

write_file = open("text.html", "w", encoding="utf_8_sig")
for url in url_list:
    if url.strip() != "":
        replaced_url = url.replace("/race/", "/odds/").replace("result.html", "index.html").replace("rf=race_list", "rf=race_submenu")
        req = requests.get(replaced_url)
        result = BeautifulSoup(req.text, "html.parser")
        print(result)
        write_file.write(result.text)
        table = result.find("table", {"id": "Ninki"})
        trs = table.findAll("tr")
        for tr in trs:
            tds = tr.findAll("td")
            if (len(tds) > 0):
                name = tds[4].find("a").text
                odds = tds[5].find("span").text
                prize_odds = tds[6].find("span").text
                prize_odds_from = prize_odds.split("-")[0].strip()
                prize_odds_to = prize_odds.split("-")[1].strip()
                # print("%s, %s, %s, %s" % (name, odds, prize_odds_from, prize_odds_to))

