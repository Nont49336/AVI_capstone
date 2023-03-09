import os
import cv2
import shutil
import numpy as np
import pandas as pd
#  this is the program to check duplicate image

path_oriimage  = "../dataset/original_image"
path_oriexcel  = "../dataset/original_excel/BN1-Streaming-20220815.xlsx"
path_rename    = "../dataset/image_identify"
path_unrename  = "../dataset/image_unidentify"

df = pd.read_excel(path_oriexcel)
n_df = len(df)

count = 0
for i in range(2771):
    for j in range(i+1, 2771):
        if (df.at[i,'3digit']==df.at[j,'3digit']) and (df.at[i,'4digit']==df.at[j,'4digit']):
            print(f"{i} \t{j} \t{df.at[i,'3digit']} \t{df.at[i,'4digit']}")
            count+=1
print(count)

