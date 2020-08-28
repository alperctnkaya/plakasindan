import requests
import random
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36', }

def getProxyList():
    url = "https://free-proxy-list.net/"

    soup = BeautifulSoup(requests.get(url).content,"html.parser")

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

def randomSession(proxies):
    session = requests.Session()
    proxy= random.choice(proxies)
    session.proxies = {"http": proxy, "https": proxy}

    return session

def getSession():
    proxies = getProxyList()

    while True:
        session = randomSession(proxies)
        try:
            response = session.get("https://sahibinden.com", timeout=1, headers = HEADERS)
            break
        except:
            continue

    return session