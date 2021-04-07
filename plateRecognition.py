from openalpr import Alpr
import sys
import requests
from bs4 import BeautifulSoup
import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36', }

url = "https://sahibinden.com/ilan/vasita-otomobil-audi-2012-a1-1.4-tfsi-122-ps-ambition-kazasiz-44.000-km-de-4-kapi-849907460/detay"
page = requests.get(url, headers = HEADERS)
soup = BeautifulSoup(page.content, "html.parser")

def recognizePlate(imgPath):

    alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data/")

    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)
    alpr.set_top_n(30)
    alpr.set_default_region("tr")

    results = alpr.recognize_file(imgPath)

    plateNumber = None
    confidence = None

    i = 0
    for plate in results['results']:
        i += 1
        for candidate in plate['candidates']:

            if candidate["plate"][0:2].isdigit():
                if candidate["plate"][2:5].isalpha():
                    candidate["plate"]=candidate["plate"][:5]+candidate["plate"][5:].replace("o","0").replace("O","0")
                    if (len(candidate["plate"][5:]) == 2 or len(candidate["plate"][5:]) == 3) and candidate["plate"][5:].isdigit():
                        candidate["matches_template"] = 1
                elif candidate["plate"][2:4].isalpha():
                    candidate["plate"]=candidate["plate"][:4]+candidate["plate"][4:].replace("o", "0").replace("O", "0")

                    if (len(candidate["plate"][4:]) == 3 or len(candidate["plate"][4:]) == 4) and candidate["plate"][4:].isdigit():

                        candidate["matches_template"] = 1


            prefix = "-"
            if candidate['matches_template']:
                prefix = "*"
            if candidate["plate"] and prefix == "*":
                plateNumber = candidate["plate"]
                confidence = candidate["confidence"]
                break
            #print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))


    alpr.unload()
    return  plateNumber


def saveImage(imgUrl, imgName, req):
    response = req.request(imgUrl)
    file = open("./plates/"+imgName,"wb")
    file.write(response.content)
    file.close()

def extractImageUrls(soup):
    imgUrls = []
    for d in soup.find_all("div", {"class": "classifiedDetailMainPhoto"}):
        for img in d.find_all("img", {"data-src":True}):
            imgUrls.append(img["data-src"])
    imgUrls.append(soup.find("img",{"class":"stdImg"})["src"])
    return imgUrls

def extractPlateNumber(soup = None, req = None, url=None):
    if url != None:
        page = req.request(url)
        soup = BeautifulSoup(page.content, "html.parser")

    imgUrls= extractImageUrls(soup)

    for url in imgUrls:
        saveImage(url,"adImage.jpg", req)
        plateNumber = recognizePlate("./plates/adImage.jpg")
        if plateNumber:
            os.rename("./plates/adImage.jpg", "./plates/"+plateNumber+".jpg")
            break

    return plateNumber