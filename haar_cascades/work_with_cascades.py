#!/usr/bin/env python

import cv2, os
import numpy as np
from PIL import Image

def recognize(photo, cascades):
	number_classes = 21
	all_cascades = {}
	numbers = {}
	#create cascades
	for key, name_cascade in cascades:
		all_cascades.update([key, cv2.CascadeClassifier(name_cascade)])
	#recognizer = cv2.createLBPHFaceRecognizer(1,8,8,8,123)

	#Create an image and bring it to an array
	gray = Image.open(photo).convert('L')
	image = np.array( gray, 'uint8' )

	#Each cascade checks the image
	for i in range(number_classes):
		coordinates = all_cascades[i].detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
		#if the cascade has found something, then add it to the dictionary and display it on the screen
		if len(coordinates) != 0:
			numbers.update([i, coordinates])
			for (x, y, w, h) in faces:
				cv2.imshow("", image[y: y + h, x: x + w])
				cv2.waitKey(50)
	return numbers

