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


path = "./cv_result/fake_image/90.jpg"
img = cv2.imread(path)
img1 = img.copy()
for i in range(4,14):
    dir_string = pytesseract.image_to_string(img, config=f'--psm 13 --oem 1', lang='tha', output_type=Output.DICT)
    # word_data = "".join([str(i) for i in dir['text']])
    word_string = dir_string['text']
    print("text:",word_string)