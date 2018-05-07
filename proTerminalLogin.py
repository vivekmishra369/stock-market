import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json 
import time
import pyautogui
import pandas as pd

global driver, refDict, megalist

megalist = []
refDict = {
    'symbol':'',
    'ltp':'',
    'change':'',
    'pchange':'',
    'bid':'',
    'ask':'',
    'bidqty':'',
    'askqty':'',
    'volume':'',
    'lut':'',
    'ltq':'',
    'totalBuySize':'',
    'totalSellSize':''
}



def login():
    global driver
    with open("credentials.json") as f:
        credentials = json.load(f)
    f.close()
    chromedriver = "/home/mike/Desktop/everything/trading/chromedriver" # chromedriver
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.get('chrome://settings/')
    driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.33);')
    driver.get("https://proterminal.hdfcsec.com/PlatformWeb/Platform/Login/userLogIn")
    userName = driver.find_element_by_id('username')
    userName.send_keys(credentials['login'])
    password = driver.find_element_by_id('password')
    password.send_keys(credentials['password'])
    dob = driver.find_element_by_id('dateofbirth')
    dob.send_keys(credentials['dob'])
    signInButn = driver.find_element_by_xpath('//*[@id="btnSignIn"]') # driver.find_element_by_class_name('loginnow')
    signInButn.click()
    time.sleep(1)
    print('signing in...')
    signInButn.click()
    pyautogui.moveTo(864,334,duration=1)
    pyautogui.click(x=864, y=334, clicks=1, button='left')
    print('signed in !')


def openWatchList():
    global driver
    bseEquity = driver.find_element_by_xpath('//*[@id="watchlistCollection"]/optgroup[2]/option[2]')
    bseEquity.click()
    mostActive = driver.find_element_by_id('watchListFilters').find_element_by_xpath('//*[@id="watchListFilters"]/option[1]')
    mostActive.click()


def collectData():
    # gc = driver.find_element_by_class_name('grid-canvas')

    while(1):
        rawData = driver.find_element_by_class_name('grid-canvas').text
        print(rawData)


def collectOneDF():
    global refDict, megalist
    for scripId in range(1,51):
        rawScripData = driver.find_element_by_xpath('//*[@id="watchlistGrid"]/div[5]/div[1]/div['+str(scripId)+']')
        scripDataListed = rawScripData.text.split('\n')
        refDict = {
            'symbol':'',
            'ltp':'',
            'change':'',
            'pchange':'',
            'bid':'',
            'ask':'',
            'bidqty':'',
            'askqty':'',
            'volume':'',
            'lut':'',
            'ltq':'',
            'totalBuySize':'',
            'totalSellSize':''
        }
        refDict['symbol'] = scripDataListed[0]
        print("======================================================")
        print(refDict['symbol'] )
        try:
            refDict['ltp'] = float(scripDataListed[1])
        except Exception as e:
            refDict['ltp'] = scripDataListed[1]
            print('error in ltp ',e)

        try:
            refDict['change'] = float(scripDataListed[2])
        except Exception as e:
            refDict['change'] = scripDataListed[2]
            print('error in change', e)

        try:
            refDict['pchange'] = float(scripDataListed[3].split('%')[0])
        except Exception as e:
            refDict['pchange'] = scripDataListed[3].split('%')[0]
            print('error in pchange', e)
        
        try:
            refDict['bid'] = float(scripDataListed[4])
        except Exception as e:
            refDict['bid'] = scripDataListed[4]
            print('error in bid', e)
        
        try:
            refDict['ask'] = float(scripDataListed[5])
        except Exception as e:
            refDict['ask'] = scripDataListed[5]
            print('error in ask', e)


        try:
            refDict['bidqty'] = int(scripDataListed[6].replace(',', ''))
        except Exception as e:
            refDict['bidqty'] = scripDataListed[6]
            print('error in bidqty', e)


        try:
            refDict['askqty'] = int(scripDataListed[7].replace(',', ''))
        except Exception as e:
            refDict['askqty'] = scripDataListed[7]
            print('error in askqty', e)


        try:
            refDict['volume'] = int(scripDataListed[8].replace(',', ''))
        except Exception as e:
            refDict['volume'] = scripDataListed[8]
            print('error in volume', e)

        refDict['lut'] = scripDataListed[9]

        try:
            refDict['ltq'] = int(scripDataListed[10].replace(',', ''))
        except Exception as e:
            refDict['ltq'] = scripDataListed[10]
            print('error in ltq', e)


        try:
            refDict['totalBuySize'] = int(scripDataListed[11].replace(',', ''))
        except Exception as e:
            refDict['totalBuySize'] = scripDataListed[11]
            print('error in totalBuySize', e)


        try:
            refDict['totalSellSize'] = int(scripDataListed[12].replace(',', ''))
        except Exception as e:
            refDict['totalSellSize'] = scripDataListed[12]
            print('error in totalSellSize', e)

        megalist.append(refDict)
        print("-----------------------------------------------------------------")
    
    return
                  
        
