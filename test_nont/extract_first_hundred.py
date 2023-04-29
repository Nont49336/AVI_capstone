import os
import shutil

file_path = ".././image_identify"

for root,dirs,files in os.walk(file_path):
    for i in range(0,100):
        shutil.copy(os.path.join(root,files[i]),".././first_hundred/"+files[i])