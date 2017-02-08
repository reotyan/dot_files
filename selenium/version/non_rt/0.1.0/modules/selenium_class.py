from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC

import numpy as np
import pandas as pd
import math
import sys
import time
import threading

from selenium_def import *

class Fetch(object):
    def __init__(self, price, ts=pd.Series([]), event=threading.Event(), sec=1.0, itr_num=5):
        self.sec = sec 
        self.itr_num = itr_num
        self.count = 0
        self.price = price
        self.ts = ts
        self.event = event
        self.temp = 0.0
        self.thread = threading.Thread(target=self.fetch, daemon=True)
        #self.thread.setDaemon(True)

    def start(self):
        self.event.clear()
        self.thread.start()

    def fetch(self):
        self.timer = threading.Timer(self.sec, self.fetch)
        self.timer.start()
        
        while True:
            self.temp = float_price(self.price)
            if self.temp > 0.0:
                break
        self.ts = self.ts.append(pd.Series([self.temp]), ignore_index=True)
        #self.ts = self.ts.drop(0, ignore_index=True)        
        del self.ts[0]
        self.ts = self.ts.reset_index(drop=True)
        self.event.set()
        self.event.clear()
        
    def cancel(self):
        self.timer.cancel()


class FirstFetch(Fetch):
    def start(self):
        self.event.clear()
        self.thread.start()

    def fetch(self):
        if self.count > self.itr_num:
            print(file=sys.stderr)
            print('FirstFetch completed.', file=sys.stderr)
            self.event.set()
            self.count = 0
            return
        self.timer = threading.Timer(self.sec, self.fetch)
        self.timer.start()
        
        while True:
            self.temp = float_price(self.price)
            if not self.temp < 0.0:
                break
        self.ts = self.ts.append(pd.Series([self.temp]), ignore_index=True)
        self.count += 1
        print('\033[K' + str(self.count - 1) + '/' + str(self.itr_num) + '\033[A', file=sys.stderr)

        
class Print(object):
    @staticmethod
    def print(*args):
        print(str(*args) + '\033[0m', file=sys.stderr)

        
if __name__ == '__main__':        
    print('a = Fetch()')
    a = Fetch('a')

    print('a.start()')
    a.start()

    print('time.sleep(10)')
    time.sleep(10)

    print('a.print()')
    a.print()

