import requests
from bs4 import BeautifulSoup
import time
import threading
import signal
import random


class requester:

    def __init__(self, headers=None, printRequest=False):

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
        while self.run:
            time.sleep(0.0001)
            try:
                page = requests.get(url, timeout=2, headers=self.header)

                self.requestCounter += 1
                self.totalRequest += 1
                self.rotateHeaders()
                self.checkRequestPerSecond()

                if page.status_code == 200 and "olagan-disi-kullanim" not in page.text:
                    success = True
                    break
                else:
                    print("BANNED - SLEEPING")
                    time.sleep(30)
            except:
                print("Timed Out")

        if not success:
            return -1

        return page

    def appendHeader(self, header):
        self.headersList.append(header)

    def checkRequestPerSecond(self):
        if self.requestCounter >= self.requestPerSecondLimit:
            time.sleep(random.random() * 2 + 1)
            self.requestCounter = 0

    def printTotalRequest(self):
        start = time.time()
        while (1):
            if self.run:
                print("Total Request :", self.totalRequest, "Time Evaluated: ", time.time() - start)
            time.sleep(5)

    def sigint_handler(self, signal, frame):
        print("SIGINT Singal Catched")
        self.run = False

    def rotateHeaders(self):
        self.header = self.headersList[self.headerIndex]

        self.headerIndex += 1
        if self.headerIndex == len(self.headersList):
            self.headerIndex = 0
