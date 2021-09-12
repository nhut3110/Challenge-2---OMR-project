import numpy as np
import cv2
import os
from os import listdir
from os.path import isfile, join
import pandas as pd

questionsF = 5
answersF = 5
correct_ans_col1 = []
correct_ans_col2 = []
difficult = [0 for i in range(62)]
ansAll = []
pathData = "C:/Users/ASUS/Desktop/challenge 2/dummy data/"

def split_image(image):
    r = len(image) // questionsF * questionsF 
    c = len(image[0]) // answersF * answersF
    image = image[:r, :c]
    rows = np.vsplit(image, questionsF)
    boxes = []
    for row in rows:
        cols = np.hsplit(row, answersF)
        for box in cols:
            boxes.append(box)
    return boxes