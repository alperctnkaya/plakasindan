import requests
from bs4 import BeautifulSoup
import time
import threading
import signal
import random


class requester:

    def __init__(self, proxy=None, headers=None, printRequest=False):

        self.proxies = proxy
        if proxy:
            self.session = self.getSession()
        else:
            self.session = requests.Session()

        self.headersList = headers
        self.headerIndex = 0
        self.header = self.headersList[self.headerIndex]

        self.requestCounter = 0
        self.requestPerSecondLimit = 1
        self.totalRequest = 0

        self.run = True

        if printRequest:
            self.requestCountThread = threading.Thread(target=self.printTotalRequest)
            self.requestCountThread.daemon = True
            self.requestCountThread.start()

        signal.signal(signal.SIGINT, self.sigint_handler)

    def request(self, url):

        success = False
        page = None

        while self.run:
            time.sleep(0.0001)
            try:
                page = self.session.get(url, timeout=2, headers=self.header)

                self.requestCounter += 1
                self.totalRequest += 1
                self.checkRequestPerSecond()

                if page.status_code == 200 and "olagan-disi-kullanim" not in page.text:
                    success = True
                    break
                else:
                    if self.proxies:
                        self.proxies.suspendProxy(self.session.proxies["https"])
                        self.session = self.getSession()
                    else:
                        print("BANNED - SLEEPING")
                        time.sleep(30)
            except:
                print("Timed Out")

        if not success:
            return -1

        return page

    def getSession(self):
        session = requests.Session()
        while True:
            proxy = self.proxies.proxyGenerator()
            session.proxies = {"http": proxy, "https": proxy}
            try:
                response = session.get("https://sahibinden.com", timeout=3, headers=self.header)
                if response.status_code == 200 and "olagan-disi-kullanim" not in response.text:
                    break
            except:
                print(session.proxies, " Failed: Proxy Suspended")
                self.proxies.suspendProxy(proxy)

        return session

    def checkRequestPerSecond(self):
        if self.requestCounter >= self.requestPerSecondLimit:
            time.sleep(random.random() * 2 + 1)
            self.requestCounter = 0

    def printTotalRequest(self):
        start = time.time()
        while 1:
            if self.run:
                print("Total Request :", self.totalRequest, "Time Evaluated: ", time.time() - start)
            time.sleep(5)

    def sigint_handler(self, signal, frame):
        print("SIGINT Singal Catched")
        self.run = False
