#!/usr/bin/python3
# highとlowの幅によって???
# openとcloseも使う???
# openとlow(high)の関係からトレンドを判断???
# if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): を生のelementに置き換える???
# 最初のwindowを閉じるようにする???
# Fedoraでテストするときのxvfbのサイズを縦長にする。firefoxのプロファイルを約定履歴を表示するようにへんこうする。!!!
# posが0なのにポジションを持っていることになっている場合がある。!!! -> スリッページの問題???
# 注文が約定しなかったときに表示されたerrエリアが、長時間消えていないので消すようにする!!!
# contract(じゃなくてorder?)の色を反転させる???
# pos_count の値によって損切りの挙動をコントロールする???
# Fetchにタイマーを設定する???
# datetimeのタイムゾーン設定???
# mailを送るようにする???
# float_priceの例外処理を無くす???
# 買い(売り)待ちの時間が長いのはもったいない。特に急なトレンドの時。???
DEBUG = True
Lot = '1'
sec = 1.0 # fetchの間隔(秒)
sec_limit = sec - 3*sec/60.0 ####
LOOP_MAX = 50 ##
ON_OFF_slippage = True # Trueならスリッページを0.1pipsに設定する
# EWMAのスパン
SPAN_S = 5
SPAN_M= 9
SPAN_L = 13
SPAN_LL = 30
itr_num = SPAN_L # FirstFetchの繰り返し回数
#
limit_count_los = 1
#
ts = None
#
n = 0
foo = 0
#============================================================
def main_loop(first_pos):
    pos = first_pos
    while True:
        count_loop += 1
        if count_loop > LOOP_MAX:
            break
        event.wait()
        ts = F.ts
        count_loop = F.count ##        
        #
        start = time.time()
        S = ts.ewm(span=SPAN_S).mean().values[-1]
        M = ts.ewm(span=SPAN_M).mean().values[-1]
        L = ts.ewm(span=SPAN_L).mean().values[-1]
        #ポジが0なら。。。
        if pos == 0:
           #買う？売る?
            if S > M > L or S < M < L:
                if S > M > L:
                    next_pos = 1; color = C.R; test = 'price > S - spread'; button = button_ask;
                elif S < M < L:
                    next_pos = 2; color = C.B; test = 'price < S + spread'; button = button_bid;                    
                P.print(str(count_loop) + ' ' + color + 'S' + C.RESET + ': {0:6.3f}'.format(S))
                while True:
                    if (time.time() - start) > sec_limit:
                        break
                    price = float_price(price_bid)
                    if eval(test):
                        continue
                    button.click()
                    try:
                        wait.until(EC.visibility_of(notice_contract_OK)) #### clickableにする???
                    except: #  selenium.common.exceptions.TimeoutException:
                        P.print('error contract!', file=2) ##
                        continue
                    else:
                        pos = next_pos
                        price_contract = price
                        P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + color + 'contract')
                        break
            #そのまま?    
            else:
                P.print(str(count_loop) + ' ' + 'S' + C.RESET + ': {0:6.3f}'.format(S))
                continue
           
        #ポジションを持っているなら。。。
        elif pos in (1, 2):
            if pos == 1:
                color = C.R; test = 'S > M'; test2 = 'price < S + diff_order_spread';
            elif pos == 2:
                color = C.B; test = 'S < M'; test2 = 'price > S - diff_order_spread';
            P.print(str(count_loop) + ' ' + color + C.BOLD + 'S' + C.RESET + ': {0:6.3f}'.format(S)) ###
            #継続?
            if eval(test): ###
                continue
            #決済する?
            else:
                price = float_price(price_bid)
                price_open = price
                price_high = price
                price_low = price
                while True:
                    # waitに間に合うようにチェック
                    if (time.time() - start) > sec_limit:
                        count_los += 1
                        # 損切り???
                        if count_los >= limit_count_los: ####
                            while True:
                                # 関数にする???
                                button_order_all.click()
                                time.sleep(sleep_order_loop) ####
                                if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできるなら
                                    continue
                                else:
                                    pos = 0 
                                    P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + color + 'ordered') ###
                                    break
                         # 急なトレンドによって損切りが発生したと仮定して、ポジションを反転させる
                         ####
                        break
                    price = float_price(price_bid)
                    # highとlowを更新
                    if price_high < price:
                        price_high = price
                    if price_low > price:
                        price_low = price
                    # orderするかチェック
                    if eval(test2): ###
                        continue
                    else:
                        button_order_all.click()
                        time.sleep(sleep_order_loop) ####
                        if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできるなら
                            continue
                        else:
                            pos = 0 
                            P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + color + 'ordered') ###
                            break
        else:
            raise Exception('pos == 3 ???')
#============================================================
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
#
import numpy as np
import pandas as pd
import math
import sys
import time
import threading
import re
import datetime
import traceback
#import seaborn
#
from selenium_def import *
from selenium_class import *
import colors as C
#============================================================
ID = 
PASSWORD = 
LOGIN_URL = 'https://demotrade.fx.dmm.com/fxcrichpresen/webrich/direct/login'
PROFILE = '/home/reosan/.mozilla/firefox/i1zq2uyh.selenium'
MAIL_ADDRESS = ''
#------------------------------------------------------------
def logout_except():
    count = 0
    '''
    while True:
        count += 1
        button_order_all.click()
        time.sleep(1)
        if not re.match(r'.*disable.*', button_order_all.get_attribute('class')):
            if count > 10:
                raise Exception('CAN NOT ORDER !!! in logout_except()')
            continue
        else:
            break
    count = 0
    '''
    while True:
        count += 1
        button_logout.click()
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@uifield="okButton"]')))
        except selenium.common.exceptions.TimeoutException:
            if count > 10:
                raise Exception('CAN NOT click button_logout !!! in logout_except()')
            continue
        else:
            break
    button_logout_OK.click()
    wait_5.until(EC.number_of_windows_to_be(1))
    window = driver.window_handles[-1]
    driver.switch_to_window(window)
    driver.quit()
#========================[START]====================================
P = Print()
# DMMへのログイン処理
try:
    profile = webdriver.FirefoxProfile(PROFILE)
    driver = webdriver.Firefox(firefox_profile=profile)
    wait = WebDriverWait(driver, 1)
    wait_5 = WebDriverWait(driver, 5)    
    wait_10 = WebDriverWait(driver, 10)
    wait_20 = WebDriverWait(driver, 20)
    wait_50 = WebDriverWait(driver, 50)
    wait_no_except = WebDriverWait(driver, 1, ignored_exceptions=True)
    wait_5_no_except = WebDriverWait(driver, 5, ignored_exceptions=True)    
    wait_10_no_except = WebDriverWait(driver, 10, ignored_exceptions=True)
    wait_20_no_except = WebDriverWait(driver, 20, ignored_exceptions=True)
    '''
    driver.implicitly_wait(10)
    '''
    P.print('connecting DMM...', file='err') 
    #
    driver.get(LOGIN_URL)
    driver.find_element_by_id('accountId').send_keys(ID)
    driver.find_element_by_id('password').send_keys(PASSWORD)
    driver.find_element_by_id('LoginWindowBtn').click()
    #
    wait_20.until(EC.number_of_windows_to_be(2))
    window = driver.window_handles[-1]
    driver.get('http://www.google.co.jp')
    driver.switch_to_window(window)
    '''
    driver.maximize_window()
    '''
    wait_get_elem_xpath(wait_50, '//div[@uifield="spread"]') ##
    elem_spread = wait_get_elem_xpath(wait_50, '//div[@uifield="spread"]')
    price_bid = wait_get_elems_xpath(wait_20, '//div[@uifield="bidStreamingButton"]/div/*')    
    price_ask = wait_get_elems_xpath(wait_20, '//div[@uifield="askStreamingButton"]/div/*')
    button_order_all = wait_get_elem_xpath(wait_20, '//button[@uifield="orderButtonAll"]')
    button_order_bid = wait_get_elem_xpath(wait_20, '//button[@uifield="orderButtonSell"]')
    button_order_ask = wait_get_elem_xpath(wait_20, '//button[@uifield="orderButtonBuy"]')    
    button_bid = wait_get_elem_xpath(wait_20, '//div[@uifield="bidStreamingButton"]')
    button_ask = wait_get_elem_xpath(wait_20, '//div[@uifield="askStreamingButton"]')
    button_slippage = wait_get_elem_xpath(wait_20, '//span[@uifield="slippageButton"]')
    text_order_Lot = wait_get_elem_xpath(wait_20, '//input[@uifield="orderQuantity"]')
    button_logout = wait_get_elem_xpath(wait_20, '//div[@class="logout label"]')
    button_logout.click()
    button_logout_OK = wait_get_elem_xpath(wait_20, '//button[@uifield="okButton"]')
    button_logout_cancel = wait_get_elem_xpath(wait_20, '//button[@uifield="cancelButton"]')
    button_logout_cancel.click()
    notice_contract_err = wait_get_elem_xpath(wait_20, '//div[@uifield="errorArea"]')
    notice_contract_OK = wait_get_elem_xpath(wait_20, '//div[@class="logout label"]')
    info_PL_today = wait_get_elem_xpath(wait_20, '//span[@uifield="dailyPlTotalJPY"]')
except:
    P.print(C.R + C.BOLD + 'CAN NOT CONNECT DMM !!!', file='err')
    logout_except()
    raise
else:
    P.print('\033[A' + '\033[K' + '\033[A', file='err') # connecting DMM を消す

    
# ログイン直後のポジションチェック
if re.match(r'.*disable.*', button_order_all.get_attribute('class')):
    pos = 0
elif not re.match(r'.*disable.*', button_order_ask.get_attribute('class')) and re.match(r'.*disable.*', button_order_bid.get_attribute('class')): # askだけクリック可
    pos = 1
elif not re.match(r'.*disable.*', button_order_bid.get_attribute('class')) and re.match(r'.*disable.*', button_order_ask.get_attribute('class')): # bidだけクリック可
    pos = 2
elif not re.match(r'.*disable.*', button_order_ask.get_attribute('class')) and not re.match(r'.*disable.*', button_order_bid.get_attribute('class')): # ask、bidの両方クリック可
    pos = 3
else:
    logout_except()
    raise Exception(C.Y + C.BOLD + 'CAN NOT DITECT POSITION')


P.print('first position: {0}'.format(pos_to_position(pos)))


# ロット、スリッページの設定
try:
    for i in range(3):
        text_order_Lot.send_keys(Keys.BACK_SPACE)
    text_order_Lot.send_keys(Lot)
    if ON_OFF_slippage:
        button_slippage.click()
except:
    P.print(C.R + 'CAN NOT SETTING DMM !!!', file='err')
    logout_except()
    raise


# FirstFetch
ts = pd.Series([])
event = threading.Event()
FF = FirstFetch(price_bid, ts=ts, itr_num=itr_num, event=event, sec=sec)
while True:
    try:
        event.clear() #
        FF.start()
        event.wait(timeout=(itr_num*sec+60.0))
    except:
        P.print(C.R + C.BOLD + 'ERROR OCCURRED IN FirstFetch !!!', file='err')
        ts = FF.ts
        traceback.print_exc()
    else:
        P.print(FF.ts)
        break

    
ts = FF.ts    
del FF


# メインループ
try:
    F = Fetch(price_bid, ts=ts, event=event, sec=sec, itr_num=itr_num)
    F.start()
    #
    spread = 0.003 ####
    diff_order_spread = spread
    count_loop = 0
    count_los = 0
    price_contract = 0.0
    price_open = 0.0
    price_high = 0.0
    price_low = 0.0
    price_close = 0.0
    limit_count_los = limit_count_los
    sleep_order_loop = 0.1
############################################################
###########################################################
    '''
    WebDriverWait(driver, timeout=X, ignored_exceptions=True)
    EC.element_to_be_clickable()
    :before ????
    <div class="executedNotification label" uifield="executedNotification" style="display: none;">
    '''
    while True:
        count_loop += 1
        if count_loop > LOOP_MAX:
            break
        # P.print('waiting...') ##
        event.wait()
        ts = F.ts
        count_loop = F.count ##        
        #
        start = time.time()
        # spread = float(elem_spread.text) / 100.0 #### pips 表示から円になおす
        S = ts.ewm(span=SPAN_S).mean().values[-1]
        '''
        S = ts.ewm(span=SPAN_S).mean()[-1:].values[0]
        '''
        M = ts.ewm(span=SPAN_M).mean().values[-1]
        L = ts.ewm(span=SPAN_L).mean().values[-1]
        
        #ポジが0なら。。。
        if pos == 0:
           #買う？
            if S > M > L:
                P.print(str(count_loop) + ' ' + C.R + 'S' + C.RESET + ': {0:6.3f}'.format(S))
                while True:
                    if (time.time() - start) > sec_limit:
                        break
                    price = float_price(price_bid)
                    if price < 0.0:
                        continue
                    elif price > S - spread:
                        continue
                    button_ask.click()
                    try:
                        wait.until(EC.visibility_of(notice_contract_OK)) #### clickableにする???
                    except: #  selenium.common.exceptions.TimeoutException:
                        P.print('error contract!', file=2) ##
                        continue
                    else:
                        pos = 1
                        price_contract = price
                        P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + C.R + 'contract')
                        break
            #売る?
            elif S < M < L:
                P.print(str(count_loop) + ' ' + C.B + 'S' + C.RESET + ': {0:6.3f}'.format(S))                
                while True:
                    if (time.time() - start) > sec_limit:
                        break
                    price = float_price(price_bid)
                    if price < 0.0:
                        continue
                    elif price < S + spread:
                        continue
                    button_bid.click()
                    try:
                        wait.until(EC.visibility_of(notice_contract_OK))
                    except  selenium.common.exceptions.TimeoutException:
                        continue
                    else:
                        pos = 2
                        price_contract = price
                        P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + C.B + 'contract')                        
                        break
            #そのまま?    
            else:
                P.print(str(count_loop) + ' ' + 'S' + C.RESET + ': {0:6.3f}'.format(S))
                continue
           
        #1(long, 買)なら。。。
        elif pos == 1: ###
            P.print(str(count_loop) + ' ' + C.R + C.BOLD + 'S' + C.RESET + ': {0:6.3f}'.format(S))
            #継続?
            if S > M: ### 
                continue
            #決済する?
            else:
                price = float_price(price_bid)
                price_open = price
                price_high = price
                price_low = price
                while True:
                    # waitに間に合うようにチェック
                    if (time.time() - start) > sec_limit:
                        count_los += 1
                        # 損切り???
                        if count_los >= limit_count_los: ####
                            while True:
                                button_order_all.click()
                                time.sleep(sleep_order_loop) ####
                                if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできるなら
                                    continue
                                else:
                                    pos = 0 
                                    P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + C.R + 'ordered') ###
                                    break
                         # 急なトレンドによって損切りが発生したと仮定して、ポジションを反転させる
                         ####
                        break
                    price = float_price(price_bid)
                    # highとlowを更新
                    if price_high < price:
                        price_high = price
                    if price_low > price:
                        price_low = price
                    # orderするかチェック
                    '''
                    if price < 0.0: ###
                        continue
                    elif price < S + spread: ###
                        continue
                    '''
                    if price < S + diff_order_spread: ###
                        continue
                    else:
                        button_order_all.click()
                        time.sleep(sleep_order_loop) ####
                        if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできるなら
                            continue
                        else:
                            pos = 0 
                            P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + C.R + 'ordered') ###
                            break
          
        #-１(short, 売)なら。。。
        elif pos == 2:
            P.print(str(count_loop) + ' ' + C.B + C.BOLD + 'S' + C.RESET + ': {0:6.3f}'.format(S))
            #継続?
            if S < M:
                continue
            #決済する?
            else:
                price = float_price(price_bid)
                price_open = price
                price_high = price
                price_low = price
                while True:
                    # waitに間に合うようにチェック
                    if (time.time() - start) > sec_limit:
                        count_los += 1
                        # 損切り???
                        if count_los >= limit_count_los: ####
                            while True:
                                button_order_all.click()
                                time.sleep(sleep_order_loop) ####
                                if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできるなら
                                    continue
                                else:
                                    pos = 0 
                                    P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + C.B + 'ordered') ###
                                    break
                        break
                    price = float_price(price_bid)
                    # highとlowを更新
                    if price_high < price:
                        price_high = price
                    if price_low > price:
                        price_low = price
                    # orderするかチェック
                    if price < 0.0: ###
                        continue
                    elif price > S - diff_order_spread: ###
                        continue
                    else:
                        button_order_all.click()
                        time.sleep(sleep_order_loop) ####
                        if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできるなら
                            continue
                        else:
                            pos = 0 
                            P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + C.B + 'ordered') ###
                            break
            '''             
            else:
                while True:
                    if (time.time() - start) > sec_limit:
                        count_los += 1
                        break
                    price = float_price(price_bid)
                    if price < 0.0:
                        continue
                    elif price > S - spread:
                        continue
                    button_order_all.click()
                    time.sleep(0.5)
                    if not re.match(r'.*disable.*', button_order_all.get_attribute('class')): # orderボタンがクリックできるなら
                        continue
                    else:
                        pos = 0
                        P.print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + C.B + 'ordered')                        
                        break
            '''
        else:
            raise Exception('pos == 3 ???')
###########################################################
###########################################################
    F.cancel()
    del F
except:
    P.print(C.R + C.BOLD + 'ERROR OCCURRED IN LOOP !!!', file='err')
    try:
        logout_except()
    except:
        driver.quit()
        #raise
    raise

# ログアウト処理
try:
    while True:
        button_order_all.click()
        time.sleep(1)
        if not re.match(r'.*disable.*', button_order_all.get_attribute('class')):
            continue
        else:
            break
    while True:
        button_logout.click()
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@uifield="okButton"]')))
        except selenium.common.exceptions.TimeoutException:
            continue
        else:
            break
    button_logout_OK.click()
    wait_5.until(EC.number_of_windows_to_be(1))
    window = driver.window_handles[-1]
    driver.switch_to_window(window)
except:
    P.print(C.R + C.BOLD + 'CAN NOT LOGOUT !!!', file='err')
    logout_except()
    raise
else:
    P.print('logout complete.', file='err')

wait_5.until(EC.number_of_windows_to_be(1))
window = driver.window_handles[-1]
driver.switch_to_window(window)

try: ###$ driver.quit()
    driver.quit()
except:
    P.print(C.R + C.BOLD + 'CAN NOT DRIVER.QUIT() !!!', file='err')
    raise
else:
    P.print('driver.quit()', file='err')


