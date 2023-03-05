import cv2
import pytesseract
from pytesseract import Output
import os
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import argparse
import shutil
import logging
from datetime import datetime
import csv
import io
#  folder structure
# Input
# folder
# |--img1.jpg
# |--img2.jpg
# |--img3.jpg
# |--img4.jpg
# Output
# folder
# |--img1.jpg
# |--img2.jpg
# |--img3.jpg
# return result and set 
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

class Tesseract:
    #  intial tesseract param
    def __init__(self,psm=6,lang="tha",oem=3):
        self.psm = psm
        self.lang = lang
        self.oem = oem
        

    def analyze(self,src):
    # single file handling
        if (src.endswith(".jpg") or src.endswith(".png")):
            dir = pytesseract.image_to_data(src, config=f'--psm {self.psm} --oem {self.oem}',lang=self.lang,output_type=Output.DICT)
            if (dir == None):
                return print("can't detect plate and character")
            else:
                return print(dir['left'],dir['top'],dir['width'],dir['height'],dir['text'])
        else:
            # directory handling
            time_stamp  = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
            # log file initialization
            readable_logger = create_logger("readable_logger",log_file=time_stamp+"_readadble")
            text_logger = create_logger("text_logger",log_file=time_stamp+"text")
            # initialize file header
            readable_logger.info(["path","psm","oem","readable","readable(img2data)","readable(img2string)","width","height"])
            text_logger.info(["path","psm","oem","text_index","text_len","text","width","height","ref_img_path"])
            # end log file initialization
            for root,dirs,files in os.walk(src):
                for file in files:
                    path = os.path.join(root,file)
                    img = cv2.imread(path)
                    dir = pytesseract.image_to_data(img, config=f'--psm {self.psm} --oem {self.oem}', lang='tha', output_type=Output.DICT)
                    n_boxes = len(dir['text'])
                    res_img = img
                    for i in range(n_boxes):
                        (x, y, w, h) = (dir['left'][i], dir['top'][i], dir['width'][i], dir['height'][i])
                        cv2.rectangle(res_img, (x, y), (x + w, y + h), (0, 0, 0), 3)
                        print(f"text{i}: {dir['text'][i]}")
                        res_img = Image.fromarray(res_img)
                        fontpath = "./angsana.ttc" # thai font
                        font = ImageFont.truetype(fontpath,16)  #h*2) #16)
                        draw = ImageDraw.Draw(res_img)
                        
                        draw.text((x, y-h), dir['text'][i], font = font, fill = (0,0,255))
                        res_img = np.array(res_img)
                        cv2.imwrite(f'./text_result/p{self.psm}o{self.oem}/{file}/res_image_{i}.jpg', res_img)
                    n_textbox = 0
                    for i in range(n_boxes):
                        if (dir['text'][i]):  
                            print(f"Original Image: ")
                            print(f"Original Path: {path}")
                            print(f"  Text Letter: {dir['text'][i]}")
                            print(f"  Index Array: {i}")
                            print(f"  Text Number: {len(dir['text'][i])}")  ##print(f"  word_num: {dir['word_num'][i]}")
                            print(f"  Width:  {dir['width'][i]}")
                            print(f"  Height: {dir['height'][i]}")
                            # text_logger.info(["path","psm","oem","text_index","text_len","text","width","height","ref_img_path"])
                            text_logger.info([path,self.psm,self.oem,i,len(dir['text'][i]),dir['text'][i],dir['width'][i],dir['height'][i],"text_result/p{self.psm}o{self.oem}/{file}/res_image_{i}.jpg"])
                            n_textbox += 1
                        # elif (not dir['text'][i]: # elif (dir['text'][i] == ""):
                    print("\nCheck Text Readable")
                    dir_string = pytesseract.image_to_string(img, config=f'--psm 4', lang='tha', output_type=Output.DICT)
                    word_data = "".join([str(i) for i in dir['text']])
                    word_string = dir_string['text']
                    print(f"Original Image: ")
                    print(f"Original Path: {path}")
                    print(f"  word_data:   {word_data}")
                    print(f"  word_string: {word_string}")
                    if (n_textbox == 0): 
                        # (["path","psm","oem","readable","readable(img2data)","width","height","readable(img2string)"])
                        shutil.copy(path,"readabiltiy/unreadable/"+"p"+str(self.psm)+"o"+str(self.oem)+"/"+file)
                        readable_logger.info([path,self.psm,self.oem,0,word_data,word_string,img.shape[1],img.shape[0]])
                        print("  Readable: No")
                    else:                
                        shutil.copy(os.path.join(root,file),"readabiltiy/readable/"+"p"+str(self.psm)+"o"+str(self.oem)+"/"+file)
                        readable_logger.info([path,self.psm,self.oem,1,word_data,word_string,img.shape[1],img.shape[0]])
                        print("  Readable: Yes")
        # full_text = "".join([str(i) for i in dir['text']])
        # print(f"full text: {full_text}")
        # cv2.imshow('res_image', res_img)
        # cv2.waitKey(0)   

#     11:28 UNNA Excel อ่านได้ไม่ได้

# - Original Image (image)
# - Name Path (string)
# - Readable (yes-no /Binary 1-0)
# - Word from image_to_data (string เช่น กณิ6648.)
# - Word from image_to_string (string เช่น 7กถิ6648)
# - Box Image (image ขนาดเท่า original)
# 11:28 UNNA Excel ตัวอักษร width height

# - Original Image (image)
# - Name Path (string)
# - Text (string เช่น ณิ)
# - Text Number (int เช่น 2)
# - Width (int)
# - Height (int)
# - Box Image (crop image ตัวอักษร)
if __name__ == "__main__":
    # print("run mains")
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--path",help="path to file or folder")
    args = parser.parse_args()
    path = args.path
    detector = Tesseract(6,"tha",3)
    detector.analyze(path,"readable")