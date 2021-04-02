class brand():

    def __init__(self, brand, url):
        self.brand = brand
        self.brandUrl = url
        self.modelNames = []
        self.models = {}

    def appendModel(self, modelName, modelObject):
        self.models[modelName]= modelObject
        self.modelNames.append(modelName)


class model():
    def __init__(self, type, brand, modelName, url):
        self.type = type
        self.brand = brand
        self.modelName = modelName
        self.modelUrl = url
        self.serieNames = []
        self.series ={}

    def appendSerie(self,serieName, serieObject):
        self.series[serieName]=serieObject
        self.serieNames.append(serieName)

class serie():
    def __init__(self, v_type, brand, model, serieName, serieUrl):
        self.v_type = v_type
        self.brand = brand
        self.model = model
        self.serieName = serieName
        self.serieUrl = serieUrl
        self.packageNames = []
        self.packages={}

    def appendPackage(self, packageName, packageObject):
        self.packages[packageName] = packageObject
        self.packageNames.append(packageName)


class package():
    def __init__(self, v_type, brand, model, serieName, packageName, packageUrl):
        self.v_type = v_type
        self.brand = brand
        self.model = model
        self.serieName = serieName
        self.packageName = packageName
        self.packageUrl = packageUrl


class ad():
    def __init__(self):
        pass

    def setTitle(self,title):
        self.title = title

    def setAdId(self,id):
        self.id=id

    def setPlateNumber(self,plateNumber):
        self.plateNumber= plateNumber

    def setCity(self,city):
        self.city = city

    def setCounty(self,county):
        self.county = county

    def setDistrict(self, district):
        self.district = district

    def setSellerName(self,sellerName):
        self.sellerName=sellerName

    def setSellerNick(self, sellerNick):
        self.sellerNick = sellerNick

    def setSellerDateSignedUp(self,dateSignedUp):
        self.dateSingnedUp=dateSignedUp

    def setCellPhone(self,phoneNumber):
        self.phoneNumber = phoneNumber

    def setPrice(self,price):
        self.price=price

    def setCategory(self, category):
        self.category = category

    def setBrand(self,brand):
        self.brand = brand

    def setModel(self, model):
        self.model = model

    def setSerie(self,serie):
        self.serie= serie

    def setPackage(self, package):
        self.package = package

    def setImage(self, image):
        self.image = image

    def setAdDate(self, date):
        self.date = date

    def setYear(self, year):
        self.year = year

    def setFuel(self, fuel):
        self.fuel = fuel

    def setTransmission(self, transmission):
        self.transmission = transmission

    def setKM(self,km):
        self.km=km

    def setBodyType(self,bodyType):
        self.bodyType=bodyType

    def setEnginePower(self, enginePower):
        self.enginePower = enginePower

    def setEngineCapacity(self, engineCapacity):
        self.engineCapacity = engineCapacity

    def setColor(self,color):
        self.color = color
