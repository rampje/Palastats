import pytesseract as pyt
from PIL import Image
import os
import pandas as pd
import cv2
import time

pyt.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
img_dir = 'D:/Projects/Paladins/Palastats/'
img_stage_dir = 'D:/Projects/Paladins/Palastats/image stage/'

# function for cropping images of cells on the score board
def crop(opened_img, x1, x2, metric):
    y1 = 270
    for x in range(0, 10):
        stage_tuple = (x1, y1, x2, y1+40)
        file_name = metric + str(x) 
        cropped_image = opened_img.crop(stage_tuple)
        cropped_image.save(img_stage_dir + file_name + '.png')
        y1 += 60
        if x == 4:
            y1 +=  15
            
# function to apply image processing and ocr
def process_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.fastNlMeansDenoising(img)
    img = cv2.GaussianBlur(img, (1,1 ), 0)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _ , img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    #_ , img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    cv2.imwrite(img_path, img)
    txt = pyt.image_to_string(img)#config = '--psm 8 -c tessedit_char_whitelist=0123456789')
    return(txt)
    
            
# create staging data to loop through
coords_df = pd.DataFrame(
       {'healing': [1525, 1525 + 115],
       'shielding' : [1380, 1380 + 115],
       'damage' : [1235, 1235 + 115],
       'objective': [1120, 1120 + 90],
       'streak' : [1000, 1000 + 90],
       'kda': [830, 830 + 130],
       'credit' : [718, 718 + 90],
       'name' : [300, 300 + 250]}
       )
coords_df = coords_df.transpose()

# create image names to loop over
image_metrics = []
for row in coords_df.iterrows():
    for x in range(0, 10):
        image_metrics.append(row[0] + str(x))

# loop through each main image applying functions
t0 = time.time()
data = []
image_files = os.listdir(img_dir + '/saved/')
for file in image_files:
    image_obj = Image.open(img_dir + '/saved/' + file)
    
    outcome = image_obj.crop((50, 20, 280, 70))
    outcome.save(img_stage_dir + 'outcome.png')
    o = process_image(img_stage_dir + 'outcome.png')
    
    details = image_obj.crop((50, 70, 900, 90))
    details.save(img_stage_dir + 'details.png')
    d = process_image(img_stage_dir + 'details.png')
    
    for row in coords_df.iterrows():
        crop(image_obj, row[1][0], row[1][1], row[0])
        timestamp = file.replace('.png', '')
        
    for x in image_metrics:
        txt = process_image(img_stage_dir + x + '.png')
        data.append([timestamp, x, txt, o, d])
        print([timestamp, x, txt, o, d])
        
print((time.time() - t0)/60)

# save built list to dataframe
df = pd.DataFrame(data, columns=['timestamp','metric','value','outcome','details'])
df.to_csv(img_dir + 'AllData_Long.csv', index = False)