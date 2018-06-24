import cv2
import pandas as pd

img = cv2.imread('D:/Projects/Paladins/Palastats/saved/20180623 122151.png')

def draw_rects(img, x1, x2):
    y1 = 270
    for x in range(0, 10):
        img = cv2.rectangle(img, (x1, y1), (x2, y1+40), (0,255,0), 1)
        y1 += 60
        if x == 4:
            y1 +=  15
    return(img)


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

cv2.imwrite('D:/Projects/Paladins/Palastats/template.png', img)





