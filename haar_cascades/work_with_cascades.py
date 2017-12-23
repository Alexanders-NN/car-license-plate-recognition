#!/usr/bin/env python

import cv2, os, sys
import numpy as np
from PIL import Image, ImageDraw 

def recognize(photo, cascades):
	number_classes = 21
	all_cascades = {}
	symbols = {}

	#for key, name_cascade in cascades:
	for i in range( number_classes ):
		new_cascade = cv2.CascadeClassifier( cascades[i] )
		all_cascades[i] = new_cascade

	#Create an image and bring it to an array
	gray = Image.open(photo).convert('L')
	#image = np.array( gray, 'uint8' )
	image = np.array( gray )

	#Each cascade checks the image
	for i in range(number_classes):
		obj = all_cascades[i].detectMultiScale( image, scaleFactor=1.1, minNeighbors=5, minSize=(10, 15) )
		#if the cascade has found something, then add it to the dictionary and display it on the screen
		if len(obj) != 0:
			symbols[i] = obj
			for (x, y, w, h) in obj:
				cv2.imshow("", image[y: y + h, x: x + w])
				cv2.waitKey(0)
	return symbols

def add_cascade(path):
	name = "cascade.xml"
	for cascade in os.listdir(path):
		if cascade == name:
			cascade = os.path.join(path, cascade)
			if os.path.isfile(cascade):
				return cascade


def main():
	photo = sys.argv[1]
	path_to_cascades = sys.argv[2]
	cascade_dict = {}
	img = Image.open(photo)
	img.show()	
	for obj in os.listdir(path_to_cascades):
		label = int( obj.split('_')[-1] )
		#label = 0
		obj = os.path.join(path_to_cascades, obj)
		cascade_dict[label] = add_cascade(obj)
	print( recognize(photo, cascade_dict) )

if __name__ == '__main__':
    main()