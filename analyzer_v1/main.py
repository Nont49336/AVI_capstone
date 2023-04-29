from func import Tesseract
import os
# start initialization

path2file = ".././first_processed"
# if os.path.isdir():
#     assert 
for i in [1,3]:
    for j in [1,3]:
        model = Tesseract(psm=j,lang="tha",oem=i)
        model.analyze(path2file)
