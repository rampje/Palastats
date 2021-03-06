# Palastats

The game [Paladins](https://www.paladins.com/) provides a lot of data at the end of each match. This data can be extracted using computer vision tools. The focus of this repository is to build a Paladins match data set and explore the determinants of match outcomes.

There are two main scripts I'm using to build my dataset:

* **Stats Saver.py** runs while I play. It detects when the end game screen appears after a match. When it detects this screen, it selects the Scoreboard tab and saves a .png of the screen. The script accomplishes this using [pyautogui](http://pyautogui.readthedocs.io/en/latest/index.html) and [pytesseract](https://github.com/madmaze/pytesseract).

* **Image2Data.py** loops through the saved .png's extracting data and putting it into a .csv. Cropped images are generated and then processed using [OpenCV](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html). The content of the processed images are then read using pytesseract and saved to a [pandas](https://pandas.pydata.org/pandas-docs/stable/) dataframe. 

---

Below is an example of the Scoreboard at the end of a match. The green frames represent all the sections that are cropped and processed for character recognition:

![](example/template.png)

---

The strategy behind pulling data from an image like the one above is to define regions of the image to crop in order to read the data of interest. Some of the cropped regions require image processing techniques including [thresholding](https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html) in order for the optical character reader from pytesseract to read the data accurately. 

For example, the chunk of data on the scoreboard representing team damage does not have a clear background. Applying some of the image processing functions available in OpenCV makes the image readable:

Before          |  After 
:-------------------------:|:-------------------------:
![](example/outcome1.png)  |  ![](example/outcome2.png)
![](example/details1.png)  |  ![](example/details2.png) 


---

## Analysis

I'm building out an R Markdown file exploring the data set. Currently it's a work in progress.

![](example/graph1.png)

![](example/graph2.png)