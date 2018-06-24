import pytesseract as pyt
from PIL import Image
import os
import pandas as pd
import cv2

pyt.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
img_dir = 'D:/Projects/Paladins/Palastats/'
img_stage_dir = 'D:/Projects/Paladins/Palastats/image stage/'

crop_coords = { # this is based on my monitor's resolution 1920x1080
        'outcome': (50, 20, 280, 70),
        'details': (50, 70, 900, 90),
        'healing1': (1490, 250, 1650, 580),
        'healing2': (1490, 560, 1650, 900),
        'damage1': (1225, 250, 1370, 580),
        'damage2':  (1225, 560, 1370, 900),
        'kda1': (825, 250, 975, 580)
        }

# crop image in location based on metric selected
def crop(image_path, saved_location, metric):
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(crop_coords[metric])
    cropped_image.save(img_stage_dir + saved_location)

# extract data from healing and damage columns, get sum
def parse_data(img_path, output_name):
    img = cv2.imread(img_path)
    img = cv2.GaussianBlur(img, (1,1 ), 0)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _ , img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    #_ , img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    output_file = img_stage_dir + output_name
    cv2.imwrite(output_file, img)
    txt = pyt.image_to_string(img, config = '-c tessedit_char_whitelist=0123456789')
    # clean text up
    txt = txt.replace('\n', ' ').replace('c', '').replace(',', '').replace('E','0')
    txt = txt.replace('[+]', '').replace('i', '').replace('.', '')
    txt = txt.replace('N2', '').replace('HA0U', '0').replace('T155', '')
    nums = txt.split()
    nums = list(map(int, nums))
    total = sum(nums)
    return(total)
    

# get K/D/A column 
def parse_kda(img_path, output_name):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _ , img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    output_file = img_stage_dir + output_name
    cv2.imwrite(output_file, img)
    txt = pyt.image_to_string(img)
    # clean text up
    txt = txt.replace('\n', ' ').replace('c', '').replace(',', '')
    txt = txt.replace('[+]', '').replace('i', '').replace('.', '')
    nums = txt.split()
    return(nums)
    

# initialize empty lists to be columns
team_heals = []
team_damage = []
enemy_heals = []
enemy_damage = []
outcome_col = []
timestamp_col = []
kda_col = []
image_files = os.listdir(img_dir + '/saved/')
for file in image_files:
    timestamp = file.replace('.png', '')
    file = img_dir + 'saved/' + file
    
    crop(file, 'heal1-1.png', 'healing1')
    crop(file, 'heal2-1.png', 'healing2')
    crop(file, 'dmg1-1.png', 'damage1')
    crop(file, 'dmg2-1.png', 'damage2')
    crop(file, 'outcome.png', 'outcome')
    crop(file, 'kda1-1.png', 'kda1')

    outcome = cv2.imread(img_stage_dir + '/outcome.png')
    outcome = pyt.image_to_string(outcome)
    
    heal1 = parse_data(img_stage_dir + '/heal1-1.png', 'heal1-2.png')
    heal2 = parse_data(img_stage_dir + '/heal2-1.png', 'heal2-2.png')
    team_heals.append(heal1)
    enemy_heals.append(heal2)    
    team_damage.append(parse_data(img_stage_dir + '/dmg1-1.png', 'dmg1-2.png'))
    enemy_damage.append(parse_data(img_stage_dir + '/dmg2-1.png', 'dmg2-2.png'))
    outcome_col.append(outcome)
    timestamp_col.append(timestamp)
    print(file)
    print(heal1)
    print(heal2)


# put lists into dataframes
output_df = pd.DataFrame(
        {'timestamp': timestamp_col,
         'outcome': outcome_col,
         'team_damage': team_damage,
         'enemy_damage': enemy_damage,
         'team_heals': team_heals,
         'enemy_heals': enemy_heals})
    
# save dataframe to csv
output_df.to_csv(img_dir + 'Match Data.csv')