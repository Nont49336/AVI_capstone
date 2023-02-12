import cv2
import pytesseract
import os

path_to_files =  "./first_processed"
res_txt_file = "first_res.txt"
for root,dirs,files in os.walk(path_to_files):
    for file in files:
        file_path = os.path.join(root,file)
        with open("first_res.txt","a") as myfile:
            myfile.write(file_path+"\n")
        for i in range(4,14):
            print(i)
            text = pytesseract.image_to_string(file_path,config=f'--psm {i}', lang='tha')
            print("Detected license plate Number is:",text)
            with open("first_res.txt","a",encoding="utf-8") as myfile:
                myfile.write("detector type "+str(i)+":"+text)


# base line : accuracy tesseract focus on wrong character >>> analyse why ???
# next step : data prep from the analysis
# https://nanonets.com/blog/ocr-with-tesseract/ tesseract ocr
# https://medium.com/super-ai-engineer/%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%83%E0%B8%8A%E0%B9%89-tesseract-%E0%B8%97%E0%B8%B3-ocr-%E0%B8%A0%E0%B8%B2%E0%B8%A9%E0%B8%B2%E0%B9%84%E0%B8%97%E0%B8%A2-94e5c5863ae5 tesseract ocr
# https://stackoverflow.com/questions/44619077/pytesseract-ocr-multiple-config-options
#  https://medium.com/@uraibeef/%E0%B8%A1%E0%B8%B2-train-tesseract-%E0%B8%94%E0%B9%89%E0%B8%A7%E0%B8%A2-font-%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B9%80%E0%B8%A3%E0%B8%B2%E0%B8%95%E0%B9%89%E0%B8%AD%E0%B8%87%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%81%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%96%E0%B8%AD%E0%B8%B0-9c1ff483a77e