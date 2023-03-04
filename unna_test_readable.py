import cv2
import pytesseract
from pytesseract import Output
import os
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import argparse

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
class Tesseract:
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
            #directory handling
            for root,dirs,files in os.walk(src):
                for file in files:
                    img = cv2.imread(os.path.join(root,file))
            dir = pytesseract.image_to_data(img, config=f'--psm 4', lang='tha', output_type=Output.DICT)
            print(dir)
            # text_roi = (dir['left'],dir['top'],dir['width'],dir['height'],dir['text'])
            # text_marker()
            # text_marker(dir)
            n_boxes = len(dir['text'])
            res_img = img
            for i in range(n_boxes):
                (x, y, w, h) = (dir['left'][i], dir['top'][i], dir['width'][i], dir['height'][i])
                cv2.rectangle(res_img, (x, y), (x + w, y + h), (0, 0, 0), 3)
                #print(f"text{i}: {dir['text'][i]}")
                res_img = Image.fromarray(res_img)
                fontpath = "./angsana.ttc" # thai font
                font = ImageFont.truetype(fontpath,16)  #h*2) #16)
                draw = ImageDraw.Draw(res_img)
                
                draw.text((x, y-5), dir['text'][i], font = font, fill = (0,0,255))
                res_img = np.array(res_img)
            ##################################################################################################################
            print("\nCheck Text Shape")
            path = os.path.join(root,file)
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
                    print(f"  Crop Image: ")
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
            if (n_textbox == 0): print("  Readable: No")
            else:                print("  Readable: Yes")
            print(f"  Box Image:")
            cv2.imshow('res_image', res_img)

            print(f"\nDirectory of image_to_data:  \n {dir}")
            print(f"\nDirectory of image_to_string:\n {dir_string}")
            #cv2.imwrite(f'res_image_{i}.jpg', res_img)

        # full_text = "".join([str(i) for i in dir['text']])
        # print(f"full text: {full_text}")
        # cv2.imshow('res_image', res_img)
        # cv2.waitKey(0)
    def char_marker(self,dir):
        return None


path = "./first_processed"

tesseract = Tesseract(psm=6,lang="tha",oem=3)
tesseract.analyze(path)
cv2.waitKey(0)

# if __name__ == "__main__":
#     # print("run mains")
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-p","--path",help="path to file or folder")
#     args = parser.parse_args()
#     path = args.path
#     detector = Tesseract(6,"tha",3)
#     detector.analyze(path)