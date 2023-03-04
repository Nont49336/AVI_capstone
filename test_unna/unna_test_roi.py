import cv2
import pytesseract
from pytesseract import Output
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\UNNA\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

path = '.././first_license/22031800000207204010111.jpg'       # './first_license/22031800000207204010111.jpg'
img = cv2.imread(path)

psm = 4
dir = pytesseract.image_to_data(img, config=f'--psm {psm}', lang='tha', output_type=Output.DICT)
print(dir)
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
 
#cv2.imwrite('res_img.jpg', res_img)

full_text = "".join([str(i) for i in dir['text']])
print(f"full text: {full_text}")
cv2.imshow('res_image', res_img)
cv2.waitKey(0)