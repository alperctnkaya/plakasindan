from scraper import *
from plateRecognition import *

def main():

    brands,brandNames=scrapBrands()
    scrapModels(brands,["Audi"])
    scrapSeries(brands["Audi"],["A1"])
    scrapPackages(brands["Audi"].models["A1"],["1.4 TFSI"])

    return advs,  brands

if __name__ =="__main__":
    advs, brands = main()