# This script creates 2 sets of images, the first is the Scoreboard with 
# highlighted frames of interest and the 2nd is examples of cropped sections
# and the processing that is done to them

import cv2
import pandas as pd
from PIL import Image

img_example = 'D:/Projects/Paladins/Palastats/saved/20180623 122151.png'
img = cv2.imread(img_example)
example_dir = 'D:/Projects/Paladins/Palastats/example/'

def draw_rects(img, x1, x2):
    y1 = 270
    for x in range(0, 10):
        img = cv2.rectangle(img, (x1, y1), (x2, y1+40), (0,255,0), 1)
        y1 += 60
        if x == 4:
            y1 +=  15
    return(img)
    
# crop image in location based on metric selected
def crop(image_path, output_file, coords):
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(example_dir + output_file)
    
def process_image(img_path, output_name):
    img = cv2.imread(img_path)
    img = cv2.fastNlMeansDenoising(img)
    img = cv2.GaussianBlur(img, (1,1 ), 0)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _ , img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    cv2.imwrite(example_dir + output_name, img)


# --
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

for row in coords_df.iterrows():
    draw_rects(img, row[1][0], row[1][1])

# draw last two rectangles
img = cv2.rectangle(img, (50, 20), (280, 70), (0,255,0), 1)
img = cv2.rectangle(img, (50, 70), (900, 90), (0,255,0), 1)

cv2.imwrite('D:/Projects/Paladins/Palastats/example/template.png', img)

# ----------
# Create example cropped images 
crop(img_example, 'outcome1.png', (50, 20, 280, 70))
process_image(example_dir + 'outcome1.png', 'outcome2.png')

crop(img_example, 'details1.png', (50, 70, 900, 90))
process_image(example_dir + 'details1.png', 'details2.png')

