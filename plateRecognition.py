from openalpr import Alpr
import sys

alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data/")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)
alpr.set_top_n(10)
alpr.set_default_region("tr")

def recognizePlate(imgPath):

    results = alpr.recognize_file(imgPath)
    plateNumber = None
    confidence = None

    i = 0
    for plate in results['results']:
        i += 1
        for candidate in plate['candidates']:
            prefix = "-"
            if candidate['matches_template']:
                prefix = "*"
            if candidate["plate"] and prefix == "*":
                plateNumber = candidate["plate"]
                confidence = candidate["confidence"]
                break
            print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))


    alpr.unload()
    return  plateNumber, confidence
