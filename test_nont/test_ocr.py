import cv2
import pytesseract
import os

path_to_files =  ".././first_processed"
res_txt_file = "first_res.txt"
# loop through all file in the folder
for root,dirs,files in os.walk(path_to_files):
    for file in files:
        file_path = os.path.join(root,file)
        with open("first_res.txt","a") as myfile: #using the file name to be the title
            myfile.write(file_path+"\n") # write in to file 
        for i in range(4,14):
            print(i)
            text = pytesseract.image_to_string(file_path,config=f'--psm {i}', lang='tha') # extract data from license plate
            print("Detected license plate Number is:",text) # write result to file 
            with open("first_res.txt","a",encoding="utf-8") as myfile:
                myfile.write("detector type "+str(i)+":"+text+"\n") # write result to file
            
            
# check ขนาดตัวอักษรที่วัดได้ กับวัดไม่ได้ ว่าได้แค่ไหน ภาพไหนรันไม่ได้ก็คือเล็กเกินไป ถ้ารันได้ก็เก็บค่ากว้างยาวตัว 
#  2 case readable and not readable
#  readable : correct and wrong >> why it wrong >> collect the size min max 
#  not readable : not detect the character 
# base line : accuracy tesseract focus on wrong character >>> analyse why ???
# next step : data prep from the analysis 
# https://nanonets.com/blog/ocr-with-tesseract/ tesseract ocr
# https://medium.com/super-ai-engineer/%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%83%E0%B8%8A%E0%B9%89-tesseract-%E0%B8%97%E0%B8%B3-ocr-%E0%B8%A0%E0%B8%B2%E0%B8%A9%E0%B8%B2%E0%B9%84%E0%B8%97%E0%B8%A2-94e5c5863ae5 tesseract ocr
# https://stackoverflow.com/questions/44619077/pytesseract-ocr-multiple-config-options
#  https://medium.com/@uraibeef/%E0%B8%A1%E0%B8%B2-train-tesseract-%E0%B8%94%E0%B9%89%E0%B8%A7%E0%B8%A2-font-%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B9%80%E0%B8%A3%E0%B8%B2%E0%B8%95%E0%B9%89%E0%B8%AD%E0%B8%87%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%81%E0%B8%B1%E0%B8%99%E0%B9%80%E0%B8%96%E0%B8%AD%E0%B8%B0-9c1ff483a77e