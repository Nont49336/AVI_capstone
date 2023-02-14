import cv2
import pytesseract
from pytesseract import Output
import os
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import argparse

#  need to set the structure of the folders 
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
def plate_analyzer(src):
    if (src.endswith(".jpg") or src.endswith(".png")):
        print(src)
        return print("test img finish")
    else:
        for root,dirs,files in os.walk(src):
            for file in files:
                img = cv2.imread(os.path.join(root,file)) 
        dir = pytesseract.image_to_data(img, config=f'--psm 4', lang='tha', output_type=Output.DICT)
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
        cv2.imwrite(f'res_image_{i}.jpg', res_img)
    

    # full_text = "".join([str(i) for i in dir['text']])
    # print(f"full text: {full_text}")
    # cv2.imshow('res_image', res_img)
    # cv2.waitKey(0)

if __name__ == "__main__":
    # print("run mains")
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--path",help="path to file or folder")
    args = parser.parse_args()
    path = args.path
    plate_analyzer(path)
    # plate_analyzer("")