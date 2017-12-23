#!/usr/bin/env python

import cv2, os, sys
import numpy as np
from PIL import Image, ImageDraw 

def search_plate(photo, cascades):
	plates = []
	all_cascades = []

	for cascade in cascades:
		new_cascade = cv2.CascadeClassifier( cascade )
		all_cascades.append( new_cascade )

	gray = Image.open(photo).convert('L')
	image = np.array( gray )

	for cascade in all_cascades:
		plates = cascade.detectMultiScale( image, scaleFactor=1.1, minNeighbors=5, minSize=(10, 15) )
		for (x, y, w, h) in plates:
				cv2.imshow("", image[y: y + h, x: x + w])
				cv2.waitKey(0)
	print(plates)
	return plates


def search_symbols(photo, cascades):
	number_classes = 2
	all_cascades = {}
	symbols = {}

	#for key, name_cascade in cascades:
	for i in range( number_classes ):
		new_cascade = cv2.CascadeClassifier( cascades[i] )
		all_cascades[i] = new_cascade

	image = np.array( photo )

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

def create_new_image(pix, coordinates):
	start_x = coordinates[0]
	start_y = coordinates[1]
	width = coordinates[2]
	height = coordinates[3]
	new_image = Image.new( 'L', (width, height) )
	draw = ImageDraw.Draw(new_image)
	for w in range(width):
		for h in range(height):
			draw.point( (w, h), pix[start_x + w, start_y + h] )
	return new_image


def main():
	photo = sys.argv[1]
	path_to_plate_cascades = sys.argv[2]
	path_to_symbols_cascades = sys.argv[3]
	
	plate_cascade = []
	symbols_cascade_dict = {}

	img = Image.open(photo).convert('L')
	img_pix = img.load()
	img.show()

	for obj in os.listdir(path_to_plate_cascades):
		obj = os.path.join( path_to_plate_cascades, obj )
		plate_cascade.append( add_cascade(obj) )

	for obj in os.listdir(path_to_symbols_cascades):
		label = int( obj.split('_')[-1] )
		obj = os.path.join( path_to_symbols_cascades, obj )
		symbols_cascade_dict[label] = add_cascade(obj)

	plates = search_plate(photo, plate_cascade)

	all_symbols = {}
	i = 1

	for plate in plates:
		plate_image = create_new_image( img_pix, plate )
		plate_image.show()
		all_symbols[i] = search_symbols( plate_image, symbols_cascade_dict )
		i = i + 1

	print(all_symbols)

if __name__ == '__main__':
    main()