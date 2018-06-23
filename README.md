# Palastats

The game [Paladins](https://www.paladins.com/) provides a lot of data at the end of each match. This data can be extracted using computer vision tools. The focus of this repository is to build a Paladins match data set and explore the determinants of match outcomes.

There are two main scripts I'm using to build my dataset:

* **Stats Saver.py** runs while I play. It detects when the end game screen appears after a match. When it detects this screen, it selects the Scoreboard tab and saves a .png of the screen. The script accomplishes this using [pyautogui](http://pyautogui.readthedocs.io/en/latest/index.html) and [pytesseract](https://github.com/madmaze/pytesseract).

* **Image2Data.py** loops through the saved .png's extracting data and putting it into a .csv. Cropped images are generated and then processed using [OpenCV](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html). The content of the processed images are then read using pytesseract and saved to a [pandas](https://pandas.pydata.org/pandas-docs/stable/) dataframe. 

---

Currently the Scoreboard screen at the end of a match looks like this:

![](saved/20180622%20160110.png)

---

The strategy behind pulling data from an image like the one above is to define regions of the image to crop in order to read the data of interest. Some of the cropped regions require image processing techniques including [thresholding](https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html) in order for the optical character reader from pytesseract to read the data accurately. 

For example, the chunk of data on the scoreboard representing team damage does not have a clear background. Applying some of the image processing functions available in OpenCV makes the image readable:

![](image%20stage/dmg1-1.png) >>> ![](image%20stage/dmg1-2.png)

---

There are other aspects of the Scoreboard image that can be extracted. This includes **Match outcome**:

![](image%20stage/outcome.png)

Map, gamemode, and match time information can also be extracted:

![](image%20stage/details.png)