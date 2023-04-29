import os
import cv2
import shutil
import numpy as np
import pandas as pd
#  this is the program to rename image from Original to idplate

path_oriimage  = "../dataset/original_image"
path_oriexcel  = "../dataset/original_excel/BN1-Streaming-20220815.xlsx"
path_rename    = "../dataset/image_identify"
path_unrename  = "../dataset/image_unidentify"

df = pd.read_excel(path_oriexcel)

count = 0
for root,dirs,files in os.walk(path_oriimage):
    for file in files: 
        index = 0
        for imgname in df['Image_Name']:
            if  (imgname+'.jpg') == file:
                registid = str(df.at[index,'3digit']) + str(df.at[index,'4digit'])
                registpv = str(df.at[index,'Province'])
                newname  = registid + '_' + registpv + '.jpg'   #registid + '.jpg'
                print(newname)
                
                shutil.copy(os.path.join(root,file),os.path.join(path_rename,newname))
                count+=1
                break
            index+=1
        if index == len(df):
            print(f"{file} not included.")
            shutil.copy(os.path.join(root,file),os.path.join(path_unrename,file))
print("Rename Count:  ", count)
print("Rename Files:  ", len(os.listdir(path_rename)))
print("Unrename Files:", len(os.listdir(path_unrename)))
