import pyautogui as p
import pytesseract as pyt
import datetime
import time

pyt.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
img_dir = 'D:/Projects/Paladins/Palastats/saved/'

shot = p.screenshot(region=(50, 20, 230, 50))
txt = pyt.image_to_string(shot)

#p.click(1600, 80) # re-queue
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
        break