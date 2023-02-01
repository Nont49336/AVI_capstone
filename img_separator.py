import os
import cv2
import numpy
#  this is the program to extract the uncropped image to cropped image
path = "./first_license"
for root,dirs,files in os.walk(path):
    for file in files: 
        cv2.imread(os.path.join(root,file)).shape
