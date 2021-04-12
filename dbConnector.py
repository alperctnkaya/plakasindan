from mysql.connector import connect, Error
import hashlib


class dbConnector:
    def __init__(self, host, user, password, dbName):
        try:
            self.connection = connect(host=host, user=user, password=password, db=dbName)
        except Error as e:
            print(e)

        self.cursor = self.connection.cursor(buffered=True)

    def execute(self, command):
        try:
            self.cursor.execute(command)

            if "select" in command:
                result = self.cursor.fetchall()
                return result

            elif "insert" in command:
                self.connection.commit()
        except Error as err:
            print(err)


class queries:
    def __init__(self):
        self.advTable = "advertisements"
        self.brandTable = "brands"
        self.urlTable = "adUrls"
        self.trChars = {'ç': 'c', 'Ç': 'C', 'ğ': 'g', 'Ğ': 'G', 'ı': 'i', 'İ': 'I',
                        'ö': 'o', 'Ö': 'O', 'ş': 's', 'Ş': 'S', 'ü': 'u', 'Ü': 'U'}

    def insertAd(self, ad):
        columnNames = ""
        values = ''
        for column in vars(ad):
            columnNames += column + ","
            values += '"' + str(vars(ad)[column]) + '"' + ","

        columnNames = columnNames[:-1]
        values = values[:-1]
        for char in self.trChars:
            values = values.replace(char, self.trChars[char])

        sql = "insert into {} ({}) values({})".format(self.advTable, columnNames, values)

        return sql

    def insertUrl(self, url):
        hash = hashlib.md5(url.encode("utf-8"))
        columnNames = "hash, url, isScraped"
        values = '"' + hash.hexdigest() + '"' + "," + '"' + url + '"' + "," + "False"
        sql = "insert into {} ({}) values({})".format(self.urlTable, columnNames, values)
        return sql

    def insertPackage(self, package, urls):
        columnNames = ""
        values = ""
        for column in vars(package):
            columnNames += column + ","
            values += '"' + str(vars(package)[column]) + '"' + ","

        for key in urls:
            columnNames += key + ","
            values += '"' + str(urls[key]) + '"' + ","

        hash = '"' + hashlib.md5(values.encode("utf-8")).hexdigest() + '"'

        columnNames += "lastScraped, hash"
        values += "now()" + "," + hash

        sql = "insert into {} ({}) values({})".format(self.brandTable, columnNames, values)
        return sql

    def isScrapedUrl(self, url):
        hash = '"' + hashlib.md5(url.encode("utf-8")).hexdigest() + '"'
        sql = "select isScraped from {} where hash = {}".format(self.urlTable, hash)
        return sql

    def isPresentUrl(self, url):
        hash = '"' + hashlib.md5(url.encode("utf-8")).hexdigest() + '"'
        sql = "select count(hash) from {} where hash = {}".format(self.urlTable, hash)
        return sql

    def selectPageUrls(self, column="packageUrl", timeDiff=1):
        sql = "select {} from {} where exists(select timestampdiff(hour, lastScraped, now()) from {} where lastScraped \
        in (select lastScraped from {}) > {})".format(column, self.brandTable, self.brandTable, self.brandTable, timeDiff)

        return sql


def insertBrandTree(brands, q, db):

    for brand in brands:
        for model in brands[brand].models:
            if len(brands[brand].models) == 0:
                break
            for serie in brands[brand].models[model].series:
                if len(brands[brand].models[model].series) == 0:
                    break
                for package in brands[brand].models[model].series[serie].packages:
                    if len(brands[brand].models[model].series[serie].packages) == 0:
                        break

                    urls = {"brandUrl": brands[brand].brandUrl, "modelUrl": brands[brand].models[model].modelUrl,
                            "serieUrl": brands[brand].models[model].series[serie].serieUrl}
                    package = brands[brand].models[model].series[serie].packages[package]

                    sql = q.insertPackage(package, urls)
                    db.execute(sql)