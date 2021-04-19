import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime
from dbOperations import *

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36', }


def randomSession(proxies):
    session = requests.Session()
    proxy = random.choice(proxies)
    session.proxies = {"http": proxy, "https": proxy}

    return session


def getSession(proxies=None):
    if proxies is None:
        proxies = getFreeProxyList()

    while True:
        session = randomSession(proxies)
        try:
            response = session.get("https://sahibinden.com", timeout=3, headers=HEADERS)
            if response.status_code == 200 and "olagan-disi-kullanim" not in response.text:
                break
        except Error as err:
            print(err)
            print(session.proxies, " Failed")

    return session


def getFreeProxyList():
    url = "https://free-proxy-list.net/"

    soup = BeautifulSoup(requests.get(url, timeout=2).content, "html.parser")

    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue

    return proxies


class Proxy:
    def __init__(self, dbCommandExec, suspendTimeout=60 * 10):
        self.dbCommandExec = dbCommandExec

        self.proxyList = []
        self.suspendTimeout = suspendTimeout
        self.proxies = {}
        self.getProxiesFromDB()

    def addProxy(self, proxy, lastSuspended):
        self.proxyList.append(proxy)
        self.proxies[proxy["ip"] + ":" + proxy["port"]] = {"suspended": False, "lastSuspended": lastSuspended}

    def getProxiesFromDB(self):
        proxies = self.dbCommandExec.self.selectProxies()

        for row in proxies:
            proxy = {"ip": row["ip"], "port": row["port"]}
            lastSuspended = row["lastSuspended"]

            if (proxy["ip"] + ":" + proxy["port"]) not in self.proxies:
                self.addProxy(proxy, lastSuspended)

    def proxyGenerator(self):
        while True:
            for proxy in self.proxyList:
                if not self.proxies[proxy]["suspended"]:
                    return proxy
                else:
                    lastSuspended = self.proxies[proxy]["lastSuspended"]
                    if (datetime.now() - lastSuspended).total_seconds() > self.suspendTimeout:
                        self.proxies[proxy]["suspended"] = False
                        return proxy

    def suspendProxy(self, proxy):
        if proxy not in self.proxyList:
            raise Exception("Proxy not in the list")

        self.proxies[proxy]["suspended"] = True
        self.proxies[proxy]["lastSuspended"] = datetime.now()

        self.dbCommandExec.suspendProxy(proxy)
