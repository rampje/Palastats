import pyautogui as p
import pytesseract as pyt
import datetime
import time
import cv2
import pandas as pd
from PIL import Image

pyt.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
img_dir = 'D:/Projects/Paladins/Palastats/saved/'
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
		

data = []
while True:
    shot = p.screenshot(region=(50, 20, 230, 50))
    txt = pyt.image_to_string(shot)
    if 'VICTORY' in txt or 'DEFEAT' in txt:
        p.click(575, 815) # unselect chat box
        p.click(1100, 120) # select scoreboard tab
        timestamp = str(datetime.datetime.now().strftime('%Y%m%d %H%M%S'))
        outputfile = img_dir + timestamp + '.png'
        time.sleep(2)
        p.screenshot(outputfile)
        
        image_obj = Image.open(outputfile) # for now
        
        outcome = image_obj.crop((50, 20, 280, 70))
        outcome.save(img_stage_dir + 'outcome.png')
        o = process_image(img_stage_dir + 'outcome.png')
        details = image_obj.crop((50, 70, 900, 90))
        details.save(img_stage_dir + 'details.png')
        d = process_image(img_stage_dir + 'details.png')
        
        for row in coords_df.iterrows():
            crop(image_obj, row[1][0], row[1][1], row[0])
        
        for x in image_metrics:
            txt = process_image(img_stage_dir + x + '.png')
            data.append([timestamp, x, txt, o, d])
            print([timestamp, x, txt, o, d])
        
        break
		

# save built list to dataframe
new_df = pd.DataFrame(data, columns=['timestamp','metric','value','outcome','details'])

# load in main df
full_df = pd.read_csv('D:/Projects/Paladins/Palastats/AllData_Long.csv',encoding = 'cp1252')
# join new df to main
full_df = full_df.merge(new_df, how='outer')
full_df.to_csv('D:/Projects/Paladins/Palastats/AllData_Long.csv', index = False)