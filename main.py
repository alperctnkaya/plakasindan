from scraper import *
from plateRecognition import *
import pickle
from dbConnector import  *

if __name__ =="__main__":
    file = open("brands", "rb")
    brands = pickle.load(file)
    q = queries()
    db = dbConnector(host="127.0.0.1", user="root", password=passwd, dbName="db1")

    insertBrandTree(brands, q, db)

    #r = requester(headersList, True)

    pageUrls = db.execute(q.selectPageUrls(timeDiff=0))

    file = open("adUrls", "rb")
    adUrls = pickle.load(file)

    for url in adUrls:
        db.execute(q.insertUrl(url))