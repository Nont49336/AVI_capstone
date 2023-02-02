import os
import cv2
import shutil
#  this is the program to extract the uncropped image to cropped image
path = "./first_license"
count = 0
for root,dirs,files in os.walk(path):
    for file in files: 
        if (cv2.imread(os.path.join(root,file)).shape != ((486, 864, 3))): 
            # print(cv2.imread(os.path.join(root,file)))
            print(os.path.join(root,file))
            shutil.move(os.path.join(root,file),os.path.join('first_processed',file))
            count+=1
            # print(os.path.join(root,'processed',file))
        else:
            print("not included")
print("processed:",count)
print("in processed folder:",len(os.listdir('first_processed')))
