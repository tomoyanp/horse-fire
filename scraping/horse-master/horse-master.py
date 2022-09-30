# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time

f = open("horse-master.csv", "w", encoding="utf_8_sig")
f.write("name, id, father_name, mother_name, grand_father_name\n")

for index in range(1, 113):
    if (index == 1):
        req = requests.post("https://db.netkeiba.com/", {
            "sort_key": "prize",
            "sort_type": "desc",
            "pid": "horse_list",
            "list": "100",
            "under_age": "2",
            "over_age": "none",
            "act": "1"
        })
    else:
        req = requests.post("https://db.netkeiba.com/", {
            "sort_key": "prize",
            "sort_type": "desc",
            "pid": "horse_list",
            "list": "100",
            "under_age": "2",
            "over_age": "none",
            "act": "1",
            "page": "%s" % index
        })

    req.encoding = req.apparent_encoding
    result = BeautifulSoup(req.text, "html.parser")
    table = result.find("table", {"class": "nk_tb_common race_table_01"})
    trs = table.findAll("tr")

    for tr in trs:
        tds = tr.findAll("td")
        if (len(tds) > 0):
            name = tds[1].find("a").text
            name_id = tds[1].find("a").get("href").split("/")[-2]
            father = tds[6].find("a").text
            mother = tds[7].find("a").text
            grand_father = tds[8].find("a").text

            f.write("%s, %s, %s, %s, %s\n" % (name, name_id, father, mother, grand_father))

    time.sleep(10)
f.close()