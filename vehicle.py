class vehicle():

    def __init__(self, type, brand, url):
        self.type = type
        self.brand = brand
        self.brandUrl = url
        self.modelNames = []
        self.models = {}



    def setModelNames(self,modelNames):
        self.modelNames = modelNames

    def appendModel(self,modelName, modelObject):
        self.models[modelName]=modelObject


class modelClass():
    def __init__(self):
        self.modelName = None
        self.modelUrl = None
        self.serieNames = None
        self.series ={}

    def setModel(self,model):
        self.modelName = model

    def setModelUrl(self, modelUrl):
        self.modelUrl= modelUrl

    def appendSerie(self,serieName, serieObject):
        self.series[serieName]=serieObject

    def setSerieNames(self,serieNames):
        self.serieNames = serieNames

class serieClass():
    def __init__(self):
        self.serieName = None
        self.serieUrl = None
        self.packageNames = None
        self. packages={}

    def setSerie(self,serie):
        self.serieName = serie

    def setSerieUrl(self,serieUrl):
        self.serieUrl = serieUrl

    def appendPackage(self, packageName, packageObject):
        self.packages[packageName]=packageObject

    def setPackageNames(self, packageNames):
        self.packageNames = packageNames


class packageClass():
    def __init__(self):
        self.packageName=None
        self.packageUrl=None

    def setPackage(self,package):
        self.packageName = package

    def setPackageUrl(self, packageUrl):
        self.packageUrl = packageUrl

class ad():
    def __init__(self):
        self.title = None
        self.dateSignedUp = None
        self.phoneNumber = None

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

    def setPlateNumber(self,plateNumber):
        self.plateNumber = plateNumber

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

