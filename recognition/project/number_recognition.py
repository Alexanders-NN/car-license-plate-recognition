#!/usr/bin/env python

import cv2, os, sys
import numpy as np
from PIL import Image, ImageDraw
from keras import Sequential
from keras.utils import np_utils 
from keras.models import model_from_json
from keras.preprocessing import image

def search_plate(image, cascades):
	plates = np.empty((0, 4), dtype = int)
	for cascade in cascades:
		obj = cascade.detectMultiScale( image, scaleFactor=1.1, minNeighbors=5 )
		if len(obj) != 0: 
			plates = np.append(plates, obj, axis = 0)
			for (x, y, w, h) in obj:
					cv2.imshow("", image[y: y + h, x: x + w])
					cv2.waitKey(0)
	return plates

def search_symbols(image, cascades):
	number_classes = 21
	symbols = {}
	for i in range(number_classes):
		obj = cascades[i].detectMultiScale( image, scaleFactor=1.1, minNeighbors=5 )
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
				return cv2.CascadeClassifier( cascade )

def create_50_70_image(pix, coordinates):
	width_image = 50
	height_image = 70
	start_x = coordinates[0]
	start_y = coordinates[1]
	width = coordinates[2]
	height = coordinates[3]
	image = Image.new( 'L', (width_image, height_image) )
	draw = ImageDraw.Draw(image)
	for w in range(width_image):
		for h in range(height_image):
			draw.point( (w, h), pix[start_x + w, start_y + h] )
	return image


def get_pixels_image(image, coordinates):
	start_x = coordinates[0]
	start_y = coordinates[1]
	width = coordinates[2]
	height = coordinates[3]
	return image[start_y : start_y + height, start_x : start_x + width]

def create_nn_model(model_structure, model_weights):
	json_file = open( model_structure )
	loaded_model = json_file.read()
	json_file.close()
	model = model_from_json( loaded_model )
	model.load_weights ( model_weights )
	return model

def symbols_from_nn(image, symbols):
	model = create_nn_model( "nn_model.json", "nn_model.h5" )
	nn_symbols = {}
	for key, values in symbols.items():
		for coordinate in values:
			image = create_50_70_image(image, coordinate)
			pix = image.img_to_array(image)
			pix = np.expand_dims(pix, axis = 0)
			preds = model.predict(pix)
			label = np.argmax(preds)
			if label not in nn_symbols:
				nn_symbols[label] = np.array([coordinate])
			else:
				nn_symbols[label] = np.append(nn_symbols[label], [coordinate], axis = 0)
	print(nn_symbols)



def main():
	photo = sys.argv[1]

	path_to_plate_cascades = "cascade_haara/full_number/cascade"
	path_to_symbols_cascades = "cascade_haara/symbols/20x30/cascades1"	

	code_symbols = {0 : "0", 1 : "1", 2 : "2", 3 : "3", 4 : "4", 5 : "5", 6 : "6",
					7 : "7", 8 : "8", 9 : "9", 10 : "A", 11 : "B", 12 : "C", 13 : "E",
					14 : "H", 15 : "K", 16 : "M", 17 : "P", 18 : "T", 19 : "X", 20 : "Y",
					21 : "trash"}

	
	plate_cascade = []
	symbols_cascade_dict = {}
	for obj in os.listdir(path_to_plate_cascades):
		obj = os.path.join( path_to_plate_cascades, obj )
		plate_cascade.append( add_cascade(obj) )

	for obj in os.listdir(path_to_symbols_cascades):
		label = int( obj.split('_')[-1] )
		obj = os.path.join( path_to_symbols_cascades, obj )
		symbols_cascade_dict[label] = add_cascade(obj)

	all_image = {}
	for image in os.listdir(photo):
		name_photo = image
		image = os.path.join(photo, image)
		img = Image.open(image).convert('L')

		full_image_arr = np.array( img )

		plates = search_plate( full_image_arr, plate_cascade )
		all_numbers = {}
		for i in range( len(plates) ):
			plate_image = get_pixels_image( full_image_arr, plates[i] )
			all_numbers[i] = search_symbols( plate_image, symbols_cascade_dict )
			symbols_from_nn(image, all_numbers[i])

	print(all_image)

if __name__ == '__main__':
    main()