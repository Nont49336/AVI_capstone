import cv2
import os
import numpy as np
import logging
import csv
import io


class CsvFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output = io.StringIO()
        self.writer = csv.writer(self.output,quoting=csv.QUOTE_ALL,delimiter=",")
    def format(self,record):
        row_value = [res for res in record.msg]
        self.writer.writerow(row_value)
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()

def create_logger(name,log_file,level=logging.DEBUG):
     handler = logging.FileHandler(log_file+".csv",encoding="utf-8")
     handler.setFormatter(CsvFormatter())
     logger = logging.getLogger(name)
     logger.setLevel(level)
     logger.addHandler(handler)
     return logger



cascade_file = "../.././cascade/license_cascade.xml"
file_path = "../.././first_hundred/"

cascade_filter = cv2.CascadeClassifier(cascade_file)
plate_not_found = 0
i = 0
def cv2_imread_win(img_filepath):
    stream = open(img_filepath, "rb")
    bytes = bytearray(stream.read())
    numpyarray = np.asarray(bytes, dtype=np.uint8)
    return cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)

minNeighbor = 3 #waiting for the best scale result
for scale in [1.05,1.25,2.50,3.75,5,7.5,8.75]:
    print(scale)
    cv_logger = create_logger("opencvlogger","scale,"+str(scale))
    cv_logger.info(["path","detected","ref"])
    for root,dirs,files in os.walk(file_path):
        for file in files:
            path=os.path.join(root,file)
            img = cv2_imread_win(path) 
            img1 = img.copy()
            plates = cascade_filter.detectMultiScale(img,
                                                    scaleFactor = scale,
                                                    minNeighbors= minNeighbor 
                                                    )

            if len(plates) == 0:
                cv_logger.info([path,0,""])
                plate_not_found += 1
            else:
                for x,y,w,h in plates:
                    os.makedirs(f"../cv_result/scale{scale}/",exist_ok=True)
                    res_img = cv2.rectangle(img1,(x,y),((x+w),(y+h)),(255,0,0), 2)
                    # cv2.imwrite(f"../cv_result/scale{scale}/{i}.jpg",res_img)
                    cv2.imencode(".jpg",res_img)[1].tofile(f"../cv_result/scale{scale}/{file}")
                    cv_logger.info([path,1,f"cv_result/scale{scale}/{file}.jpg"])
                    i+=1
                    
    print(f"At scale {scale} : plate not found {plate_not_found} from {len(os.listdir(file_path))}")
    plate_not_found = 0
