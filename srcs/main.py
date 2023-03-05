from func import *

# start initialization

path2file = "first_processed"

for i in range(0,4):
    for j in range(0,14):
        model = Tesseract(psm=j,str="tha",oem=i)
        Tesseract.analyze(path2file)
