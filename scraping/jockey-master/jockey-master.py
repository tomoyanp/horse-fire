# coding: utf-8

import requests
from bs4 import BeautifulSoup
import json

f = open("jockey.json", "w")

jockey_id = 1
jockey_dict = {}

for index in range(1, 31):
    print(index)
    if index == 1:
        req = requests.post("https://db.netkeiba.com/", {
            "pid": "jockey_list",
            "word": "",
            "sort": "win",
            "list": "100",
            "act[]": "0",
            "act[]": "1"
        })

    else:
        req = requests.post("https://db.netkeiba.com/", {
            "sort_key": "win",
            "sort_type": "desc",
            "pid": "jockey_list",
            "word": "",
            "list": "100",
            "act[]": "0",
            "act[]": "1",
            "page": "%s" % index
        })

    req.encoding = req.apparent_encoding
    result = BeautifulSoup(req.text, "html.parser")
    print(result)
    links = result.find("div", {"class": "pager"}).findAll("a")
    next = False
    for link in links:
        if link.text == "次":
            next = True
            print("NEXT")

    table = result.find("table", {"class": "nk_tb_common race_table_01"})
    trs = table.findAll("tr")

    for tr in trs:
        tds = tr.findAll("td")
        if (len(tds) > 0):
            name = tds[0].find("a").text
            first_count = tds[3].find("a").text # 一着になった回数
            second_count = tds[4].find("a").text # 二着になった回数
            third_count = tds[5].find("a").text # 三着になった回数
            outofscope_count = tds[5].find("a").text # 着外
            jockey_dict[name] = {}
            jockey_dict[name]["first_count"] = first_count
            jockey_dict[name]["second_count"] = second_count
            jockey_dict[name]["third_count"] = third_count
            jockey_dict[name]["outofscope_count"] = outofscope_count
            jockey_dict[name]["id"] = jockey_id
            jockey_id += 1

json.dump(jockey_dict, f, indent=2, ensure_ascii=False)
f.close()