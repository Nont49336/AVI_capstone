import os
import cv2
import numpy as np
from func import *

 
# adding Folder_2 to the system path

file_path = ".././first_hundred"

def cv2_imread_win(img_filepath):
    stream = open(img_filepath, "rb")
    bytes = bytearray(stream.read())
    numpyarray = np.asarray(bytes, dtype=np.uint8)
    return cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
logger = create_logger("test_hundred","test_hundred")
logger.info(["path","psm","oem","conf","text"])
for i in [1,3]:
    for j in [1,3,4,5,6,7,8,9,10,11,12,13]:
        model = Tesseract(psm=j,lang="tha",oem=i)

        for root,dirs,files in os.walk(file_path):
            for file in files:
                path = os.path.join(root,file) 
                img = cv2_imread_win(path) 
                # 0:864,34:452
                # img = img[0:34,34:864]
                img = img[35:,:864]
                result = model.predict(img)
                logger.info([path,j,i,result[0],result[1]])

        