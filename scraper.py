from vehicle import *
from proxies import *
from plateRecognition import *
from requester import *
from bs4 import BeautifulSoup

URL = "https://www.sahibinden.com"

headersList = []


headersList.append({
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
    "Cookie": "vid=66; cdid=cX8LRliHmXW43Ghm605af0cb; MS1=https://www.google.com/; _fbp=fb.1.1616581610353.907691525; _ga=GA1.2.1228957301.1616581612; nwsh=std; showPremiumBanner=false; segIds=; OptanonConsent=isIABGlobal=false&datestamp=Thu+Apr+01+2021+11%3A50%3A49+GMT%2B0300+(GMT%2B03%3A00)&version=6.14.0&hosts=&consentId=0d17179d-0703-433c-8b89-575d5db3cd49&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A0&AwaitingReconsent=false&geolocation=TR%3B06; _gid=GA1.2.284740771.1617020639; OptanonAlertBoxClosed=2021-03-29T12:27:33.786Z; st=a84541c4b561942468995fb30a3eba0340698520ac097914358a610c9690db6eee60ad758188271022f5771df6964f0e1d3f80dbe0f2ba206; geoipCity=ankara; geoipIsp=turkcell_superonline"
})


def scrapBrandTree():

    req = requester(headersList, True)

    brands = scrapBrands(req)

    brandNames = [brand for brand in brands]

    scrapModels(brands, brandNames, req)

    for brand in brandNames:
        try:
            scrapSeries(brands[brand], brands[brand].modelNames, req)
        except Exception as err:
            print(err)
            return brands

        for model in brands[brand].modelNames:
            try:
                scrapPackages(brands[brand].models[model], brands[brand].models[model].series, req)
            except Exception as err:
                print(err)
                return brands

    return brands


def scrapBrands(req):
    brands = {}
    brandNames = []
    url = URL + "/kategori/otomobil"
    page = req.request(url)
    soup = BeautifulSoup(page.content, "html.parser")

    for _brand in soup.find_all("div", {"class": "uiInlineBoxContent category-list"}):
        for liTag in _brand.find_all("li"):
            brands[liTag.find("a").text] = brand(liTag.find("a").text, URL + liTag.find("a")["href"])

    return brands


# Audi, A1 ... A5 vs
def scrapModels(brands, brandNames, req):
    v_type = "car"
    # v_type'ı dinamik olarak al

    modelNames = []
    for brand in brandNames:

        url = brands[brand].brandUrl
        page = req.request(url)
        soupBrand = BeautifulSoup(page.content, "html.parser")
        if soupBrand == -1:
            return

        models = []
        for modelItem in soupBrand.find_all("div", {"class": "multiple-models"}):
            for liTag in modelItem.find_all("li", {"class": "cl3"}):
                model_name = liTag.find("a").text.replace("  ", "").replace("\n", "")
                model_url = brands[brand].brandUrl + "-" + liTag.find("a").text.replace("  ", "").replace("\n",
                                                                                                          "").replace(
                    " ", "-").lower()
                _model = model(v_type, brand, model_name, model_url)
                brands[brand].appendModel(_model.modelName, _model)
                models.append(_model.modelName)
        modelNames.append(models)

    return modelNames


def scrapSeries(brand, models, req):
    serieNames = []
    for model in models:
        v_type = brand.models[model].type

        url = brand.models[model].modelUrl
        page = req.request(url)
        soupModel = BeautifulSoup(page.content, "html.parser")

        if soupModel == -1:
            print("-SERIES")
            return

        series = []

        for serieItem in soupModel.find_all("div", {"class": "model"}):
            for liTag in serieItem.find_all("li", {"class": "cl4"}):
                serieName = liTag.find("a").text.replace("  ", "").replace("\n", "")
                serieUrl = brand.models[model].modelUrl + "-" + liTag.find("a").text.replace("  ", "").replace("\n",
                                                                                                               "").replace(
                    " ", "-").lower()
                _serie = serie(v_type, brand.brand, model, serieName, serieUrl)
                brand.models[model].appendSerie(_serie.serieName, _serie)
                series.append(_serie.serieName)

        serieNames.append(series)

    return serieNames


# Audi A1, series = 1.4 TFSI ...
def scrapPackages(model, series, req):
    packages = []
    brand = model.brand
    v_type = model.type

    for serie in series:

        url = model.series[serie].serieUrl
        page = req.request(url)
        soupSerie = BeautifulSoup(page.content, "html.parser")

        if soupSerie == -1:
            print("-SERIES")
            return

        packageNames = []

        for packageItem in soupSerie.find_all("div", {"class": "scroll-pane lazy-scroll"}):
            for liTag in packageItem.find_all("li", {"class": "cl5"}):
                packageName = liTag.find("a").text
                packageUrl = model.series[serie].serieUrl + "-" + liTag.find("a").text.lower()
                _package = package(v_type, brand, model.modelName, serie, packageName, packageUrl)
                model.series[serie].appendPackage(_package.package, _package)
                packageNames.append(packageName)
        packages.append(packageNames)

    return packages


def scrapAdURls(url, req):

    page = req.request(url)
    soup = BeautifulSoup(page.content, "html.parser")

    adUrls = []
    mainUrl = "https://sahibinden.com"
    for item in soup.find_all("tr", {"data-id": True}):
        adUrls.append(mainUrl + item.find("a")["href"])

    return adUrls


def scrapItem(url, req, licencePlate=True):
    page = req.request(url)
    soup = BeautifulSoup(page.content, "html.parser")

    if soup == -1:
        print("-Item")
        return
    adv = ad()

    if licencePlate:
        adv.setPlateNumber(extractPlateNumber(soup=soup, req=req))
    else:
        adv.setPlateNumber(None)

    adv.setTitle(soup.find("div", {"class": "classifiedDetailTitle"}).find("h1").text)
    adv.setAdId(soup.find("span", {"class": "classifiedId"}).text)
    adv.setSellerName(soup.find("div", {"class": "username-info-area"}).find("h5").text)
    adv.setSellerNick(soup.find("dt").text)
    if soup.find("p", {"class": "userRegistrationDate"}) is not None:
        adv.setSellerDateSignedUp(
            soup.find("p", {"class": "userRegistrationDate"}).text.replace("\n", "").replace("  ", "")[13:])
    if soup.find("span", {"class": "pretty-phone-part"}) is not None:
        adv.setCellPhone(soup.find("span", {"class": "pretty-phone-part"}).text)
    adv.setPrice(soup.find("input", {"id": "priceHistoryFlag"}).previousSibling.replace("\n", "").replace("  ", ""))
    adv.setCategory(soup.find("img")["alt"].split("/")[1])

    for ulTag in soup.find_all("ul", {"class": "classifiedInfoList"}):
        for liTag in ulTag.find_all("li", {"class": ""}):
            tag = liTag.find("strong")

            if tag.text == "Marka":
                adv.setBrand(liTag.find("span").text.replace("\xa0", "")[0])

            elif tag.text == "Seri":
                adv.setSerie(liTag.find("span").text.replace("\xa0", "")[0])
            elif tag.text == "Model":
                model = liTag.find("span").text
                adv.setModel(model.replace("\xa0", ""))
            elif tag.text == "Yıl":
                adv.setYear(liTag.find("span").text.replace("  ", "").replace("\n", "").replace("\t", ""))
            elif tag.text == "Yakıt":
                adv.setFuel(liTag.find("span").text.replace("  ", "").replace("\n", "").replace("\t", ""))
            elif tag.text == "Vites":
                adv.setTransmission(liTag.find("span").text.replace("  ", "").replace("\n", "").replace("\t", ""))
            elif tag.text == "KM":
                adv.setKM(liTag.find("span").text.replace("  ", "").replace("\n", "").replace("\t", ""))
            elif tag.text == "Kasa Tipi":
                adv.setBodyType(liTag.find("span").text.replace("  ", "").replace("\n", "").replace("\t", ""))
            elif tag.text == "Motor Gücü":
                adv.setEnginePower(liTag.find("span").text.replace("  ", "").replace("\n", "").replace("\t", ""))
            elif tag.text == "Motor Hacmi":
                adv.setEngineCapacity(liTag.find("span").text.replace("  ", "").replace("\n", "").replace("\t", ""))
            elif tag.text == "Renk":
                adv.setColor(liTag.find("span").text.replace("  ", "").replace("\n", "").replace("\t", ""))

    counter = 0
    for h in soup.find_all("h2"):
        for a in h.find_all("a", {"data-click-label": True}):
            if counter == 0:
                adv.setCity(a.text.replace("  ", "").replace("\n", ""))
            elif counter == 1:
                adv.setCounty(a.text.replace("  ", "").replace("\n", ""))
            elif counter == 2:
                adv.setDistrict(a.text.replace("  ", "").replace("\n", ""))
            counter += 1

    adv.setAdUrl(url)

    return adv
