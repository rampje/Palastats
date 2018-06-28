import pandas as pd
import numpy as np
from PIL import Image
import os
import time
import cv2

img_example = 'D:/Projects/Paladins/Palastats/saved/20180623 122151.png'
saved_dir = 'D:/Projects/Paladins/Palastats/saved/'
img_stage = 'D:/Projects/Paladins/Palastats/image stage/'
portrait_dir = 'D:/Projects/Paladins/Palastats/example/portraits/'

def crop_portraits(img):
    x1 = 162
    y1 = 266
    rows = []
    for x in range(0, 10):
        img_name = img.replace('.png', '')
        img_name = img_name.replace(saved_dir, '')
        timestamp = img_name
        img_name = img_name + '-' + str(x)
        output_f = img_stage + img_name + '.png'
        image_obj = Image.open(img)
        image_obj = image_obj.crop((x1, y1, x1+60, y1+50))
        image_obj.save(output_f)
        image1 = cv2.imread(output_f)
        diffs = []
        for image2 in portrait_matrices:
            diff_matrix = cv2.subtract(image1, image2)
            diffs.append(diff_matrix.sum())
        diffs = np.array(diffs)
        index = np.argmin(diffs)
        rows.append([timestamp, x, portrait_names[index]])
        os.remove(output_f)
        
        y1 += 61
        if x == 4:
            y1 +=  9
            
    return(rows)

# load reference portraits
portrait_matrices = []
portraits = os.listdir(portrait_dir)
portrait_names = []
for p in portraits:
    p = portrait_dir + p
    loaded_image = cv2.imread(p)
    portrait_matrices.append(loaded_image)
    portrait_names.append(p.replace('.png', '').replace(portrait_dir,''))

crop_portraits(img_example)

t0 = time.time()
image_files = os.listdir(saved_dir)
data = []
for s in image_files:
    print(s)
    data.extend(crop_portraits(saved_dir + s))

# save built list to dataframe
df = pd.DataFrame(data, columns=['timestamp','player_num','champion'])
df.to_csv('D:/Projects/Paladins/Palastats/' + 'AllChampions_Long.csv', index = False)