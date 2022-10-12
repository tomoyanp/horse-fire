# coding: utf-8
import csv
import sys
import os
import traceback
import time
from datetime import datetime,timedelta

import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_binary


dt_now = datetime.now()

# レース開催日の一覧 + kaisai_date=20200927(YYYYMMDD)
BASE_RACEDATE_URL ="https://race.netkeiba.com/top/race_list.html?"
BASE_RACE_URL     ="https://race.netkeiba.com"

def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
    return driver

def getTopPage(driver, targetURL):
    try:
        # ターゲット
        driver.get(targetURL)
        # id="RaceTopRace"の要素が見つかるまで3秒は待つ
        isExist = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, 'RaceTopRace')))
        if isExist:
            pageSource = driver.page_source
            return pageSource
    except TimeoutException:
        return None
    except Exception as e:
        print("Exception\n" + traceback.format_exc())
        return None

def getRaceIdList(pageSource):
    
    soup = bs4.BeautifulSoup(pageSource, features='lxml')
    try:
        raceIdList = []
        elem_base = soup.find(id="RaceTopRace")
        if elem_base:
            # RaceList_DataItemのli tag 全部取得
            elems = elem_base.find_all("li", class_="RaceList_DataItem")
            for elem in elems:
                # 最初のaタグを取得
                a_tag = elem.find("a")
                if a_tag:
                    # hrefタグのうち、レースIDのURLを取得
                    href = a_tag.attrs['href']
                    if ('result.html' in href):
                        raceIdList.append(BASE_RACE_URL+href.strip('.'))
        return raceIdList

    except Exception as e:
        print("Exception\n" + traceback.format_exc())
        print("レースIDの取得に失敗しました。")
        return None

if __name__ == '__main__':

    args = sys.argv

    # コマンドライン引数からレース開催日を取得する一覧を取得
    monthFrom  = args[1]
    monthTo    = args[2]

    print("Start From:"+monthFrom+" To:"+monthTo )
    print("Start Time :"+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')) 

    # 対象期間を指定
    startDate = datetime.strptime(monthFrom+'01', '%Y%m%d').date()
    endDate   = datetime.strptime(monthTo+'31',   '%Y%m%d').date()

    # Chrome Driverを取得
    googleDriver = getDriver()

    raceLists = []
    for i in range((endDate - startDate).days):
        #開催日対象日付(YYYMMDD)
        targetDate = (startDate + timedelta(i)).strftime('%Y%m%d')
        #対象URLから開催一覧の取得
        targetURL = BASE_RACEDATE_URL+'kaisai_date='+targetDate
        print("開催日付のURL:"+targetURL)
        #対象日付にレース開催があったのか確認
        pageSource = getTopPage(googleDriver,targetURL)
        if pageSource is None:
            print("対象日付に開催レースはありません")
        else:
            #対象日付にレースが開催されていれば対象ページのレースIDを全て出力
            raceLists.append(getRaceIdList(pageSource))

    #Chrome Driverは絶対殺すマン
    googleDriver.quit()

    if len(raceLists) != 0:
        with open('race_id_list.csv', 'w') as file:
            for raceList in raceLists:
                for raceId in raceList:
                    file.write("%s\n" % raceId)

    print("End TIme :"+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')) 