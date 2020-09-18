import requests
from vehicle import *
from proxies import *
from plateRecognition import *
from bs4 import BeautifulSoup
import time

URL = "https://www.sahibinden.com"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36', }

def scrapBrands():
    brands = {}
    brandNames=[]
    page = requests.get(URL + "/kategori/otomobil", headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")
    for brand in soup.find_all("div", {"class": "uiInlineBoxContent category-list"}):
        for liTag in brand.find_all("li"):
            brands[liTag.find("a").text]=vehicle("car",liTag.find("a").text,URL+liTag.find("a")["href"])
            brandNames.append(liTag.find("a").text)
    return brands, brandNames

def scrapModels(brands, brandNames):

    requestCount = 0
    for brand in brandNames:
        if requestCount % 20 == 0:
            #session = getSession()
            session = requests.Session()

        pageBrand = session.get(brands[brand].brandUrl, headers = HEADERS)
        soupBrand = BeautifulSoup(pageBrand.content,"html.parser")

        models = []
        modelNames=[]
        for modelItem in soupBrand.find_all("div",{"class":"multiple-models"}):
            for liTag in modelItem.find_all("li",{"class": "cl3"}):
                model = modelClass()
                model.setModel(liTag.find("a").text.replace("  ","").replace("\n",""))
                modelNames.append(liTag.find("a").text.replace("  ", "").replace("\n", ""))
                model.setModelUrl(brands[brand].brandUrl + "-" + liTag.find("a").text.replace("  ", "").replace("\n", "").replace(" ","-").lower())
                brands[brand].appendModel(model.modelName, model)

        brands[brand].setModelNames(modelNames)
        requestCount+=1

#Audi, A1 ...
def scrapSeries(brand, models):

    requestCount=0

    for model in models:
        if requestCount%20 == 0:
            #session=getSession()
            session = requests.Session()

        pageModel = requests.get(brand.models[model].modelUrl, headers = HEADERS )
        soupModel = BeautifulSoup(pageModel.content, "html.parser")
        series=[]
        serieNames=[]

        for serie in soupModel.find_all("div", {"class":"model"}):
            for liTag in serie.find_all("li",{"class":"cl4"}):
                serie = serieClass()
                serie.setSerie(liTag.find("a").text.replace("  ","").replace("\n",""))
                serieNames.append(liTag.find("a").text.replace("  ", "").replace("\n", ""))
                serie.setSerieUrl(brand.models[model].modelUrl+"-"+ liTag.find("a").text.replace("  ","").replace("\n","").replace(" ","-").lower())
                brand.models[model].appendSerie(serie.serieName, serie)

        brand.models[model].setSerieNames(serieNames)
        requestCount+=1

#Audi A1, series = 1.4 TFSI ...
def scrapPackages(model, series):

    requestCount=0
    for serie in series:
        if requestCount%20 == 0:
            #session=getSession()
            session=requests.Session()

        pageSerie = requests.get(model.series[serie].serieUrl, headers = HEADERS)
        soupSerie = BeautifulSoup(pageSerie.content,"html.parser")

        packages=[]
        packageNames=[]

        for package in soupSerie.find_all("div", {"class":"scroll-pane lazy-scroll"}):
            for liTag in package.find_all("li",{"class": "cl5"}):
                package = packageClass()
                package.setPackage(liTag.find("a").text)
                packageNames.append(liTag.find("a").text)
                package.setPackageUrl(model.series[serie].serieUrl+"-"+liTag.find("a").text.lower())
                model.series[serie].appendPackage(package.packageName, package)

        model.series[serie].setPackageNames(packageNames)
        requestCount+=1

def scrapItems(url):
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")
    i=0
    mainUrl = "https://sahibinden.com"
    advs=[]
    #session=getSession()

    for item in soup.find_all("tr",{"data-id":True}):
        print(mainUrl+item.find("a")["href"])
        page = requests.get(mainUrl+item.find("a")["href"], headers = HEADERS)
        soup=BeautifulSoup(page.content,"html.parser")
        adv = ad()

        adv.setPlateNumber(extractPlateNumber(soup))
        adv.setTitle(soup.find("div", {"class":"classifiedDetailTitle"}).find("h1").text)
        adv.setAdId(soup.find("span", {"class": "classifiedId"}).text)
        adv.setSellerName(soup.find("div",{"class":"username-info-area"}).find("h5").text)
        adv.setSellerNick(soup.find("dt").text)
        if soup.find("p", { "class":"userRegistrationDate"}) != None:
            adv.setSellerDateSignedUp(soup.find("p", { "class":"userRegistrationDate"}).text.replace("\n","").replace("  ","")[13:])
        if soup.find("span",{"class":"pretty-phone-part"}) != None:
            adv.setCellPhone(soup.find("span",{"class":"pretty-phone-part"}).text)
        adv.setPrice(soup.find("input", {"id":"priceHistoryFlag"}).previousSibling.replace("\n","").replace("  ",""))
        adv.setCategory(soup.find("img")["alt"].split("/")[1])

        for ulTag in soup.find_all("ul", {"class":"classifiedInfoList"}):
            for liTag in ulTag.find_all("li", {"class":""}):
                tag = liTag.find("strong")

                if tag.text == "Marka":
                    adv.setBrand(liTag.find("span").text.replace("\xa0","")[0])

                elif tag.text == "Seri":
                    adv.setSerie(liTag.find("span").text.replace("\xa0","")[0])
                elif tag.text == "Model":
                    model = liTag.find("span").text
                    adv.setModel(model.replace("\xa0",""))
                elif tag.text == "Yıl":
                    adv.setYear(liTag.find("span").text.replace("  ","").replace("\n","").replace("\t",""))
                elif tag.text == "Yakıt":
                    adv.setFuel(liTag.find("span").text.replace("  ","").replace("\n","").replace("\t",""))
                elif tag.text == "Vites":
                    adv.setTransmission(liTag.find("span").text.replace("  ","").replace("\n","").replace("\t",""))
                elif tag.text == "KM":
                    adv.setKM(liTag.find("span").text.replace("  ","").replace("\n","").replace("\t",""))
                elif tag.text == "Kasa Tipi":
                    adv.setBodyType(liTag.find("span").text.replace("  ","").replace("\n","").replace("\t",""))
                elif tag.text == "Motor Gücü":
                    adv.setEnginePower(liTag.find("span").text.replace("  ","").replace("\n","").replace("\t",""))
                elif tag.text == "Motor Hacmi":
                    adv.setEngineCapacity(liTag.find("span").text.replace("  ","").replace("\n","").replace("\t",""))
                elif tag.text == "Renk":
                    adv.setColor(liTag.find("span").text.replace("  ","").replace("\n","").replace("\t",""))

        counter = 0
        for h in soup.find_all("h2"):
            for a in h.find_all("a", {"data-click-label": True}):
                if counter == 0:
                    adv.setCity(a.text.replace("  ","").replace("\n",""))
                elif counter == 1:
                    adv.setCounty(a.text.replace("  ", "").replace("\n",""))
                elif counter == 2:
                    adv.setDistrict(a.text.replace("  ", "").replace("\n",""))
                counter +=1

        advs.append(adv)

    return advs



url = 'https://www.sahibinden.com/audi-a1-1.4-tfsi-ambition'
#models = []
#brands,brandNames=scrapBrands()
#scrapModels(brands,["Audi"])
#scrapSeries(brands["Audi"],["A1"])
#scrapPackages(brands["Audi"].models["A1"],["1.4 TFSI"])