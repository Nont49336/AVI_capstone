from func import *

# start initialization

path2file = "first_processed"

for i in [1,3]:
    for j in range(0,14):
        model = Tesseract(psm=j,lang="tha",oem=i)
        model.analyze(path2file)
