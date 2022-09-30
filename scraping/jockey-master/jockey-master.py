# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time

f = open("jockey-master.csv", "w", encoding="utf_8_sig")
f.write("name, id\n")

for index in range(1, 13):
    if index == 1:
        req = requests.post("https://db.netkeiba.com/", {
            "sort_key": "win",
            "pid": "jockey_list",
            "list": "100",
            "act[]": "0"
        })

    else:
        req = requests.post("https://db.netkeiba.com/", {
            "sort_key": "win",
            "pid": "jockey_list",
            "list": "100",
            "act[]": "0",
            "page": "%s" % index
        })

    req.encoding = req.apparent_encoding
    result = BeautifulSoup(req.text, "html.parser")
    table = result.find("table", {"class": "nk_tb_common race_table_01"})
    trs = table.findAll("tr")

    for tr in trs:
        tds = tr.findAll("td")
        if (len(tds) > 0):
            name = tds[0].find("a").text
            name_id = tds[0].find("a").get("href").split("/")[-2]

            f.write("%s, %s\n" % (name, name_id))

f.close()