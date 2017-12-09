#!/usr/bin/env python

import cv2, os
import numpy as np
from PIL import Image

def recognize(photo, cascades):
	all_cascades = {}
	numbers = []
	for key, name_cascade in cascades:
		new_cascade = cv2.CascadeClassifier(name_cascade)
		all_cascades.update([key, new_cascade])
	recognizer = cv2.createLBPHFaceRecognizer(1,8,8,8,123)
	for i in range(21):
		numbers.append( all_cascades[i].detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(10, 15)) )
	#for (x, y, w, h) in numbers:
