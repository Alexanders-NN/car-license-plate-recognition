#!/usr/bin/env python

import cv2, os, sys
import numpy as np
import Tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from math import floor
from keras import Sequential
from keras.utils import np_utils 
from keras.models import model_from_json
from keras.preprocessing import image


class ExampleApp(tk.Tk):
    current_index = 0

    scale = (1, 1) 

    viewer_scale = (0.6 , 1)
    viewer_size = (0, 0)

    x = 0
    y = 0
    rect = None
    start_x = None
    start_y = None
    end_x = None
    end_y = None

    def __init__(self, image_paths, photo_plates, photo_symbols, filename):
        tk.Tk.__init__(self)

        self.width, self.height = ( int(self.winfo_screenwidth() * 0.8), int(self.winfo_screenheight() * 0.8) )

        self.title('Car license viewer')

        self.photos_list = [name.replace('\n', '') for name in open( image_paths, 'r' )]
        #self.photos_list = image_paths

        self.plates_list = photo_plates

        self.symbols_coordinate = photo_symbols

        self.viewer_size = self.width, self.height
        self.canvas = tk.Canvas( self, 
        	width=self.viewer_size[0], 
        	height=self.viewer_size[1],
        	bg="lightblue"
        )

        self.ratio = float(self.viewer_size[0]) / self.viewer_size[1] 

        self.canvas.pack(side="top", fill="both", expand=True)

        self.bind( "<space>", self.skip )

        self.draw_image()

        #self.draw_plates()


    def draw_image(self):
    	if not self.photos_list:
    		return

    	photo = self.photos_list[self.current_index]
    	#photo = self.photos_list
        self.image = Image.open( photo )
        
        size = ( int(self.viewer_scale[0] * self.width), int(self.viewer_scale[1] * self.height) )
        
        self.resized = self.image.resize( (int(size[0]), int(size[1])), Image.ANTIALIAS )
        self.tk_image = ImageTk.PhotoImage( self.resized )

        self.canvas.create_image( 0, 0, anchor = "nw", image = self.tk_image, tags = 'image' )

        self.draw_plates(self.image.load(), self.plates_list[self.current_index])

    def draw_plates(self, image, coordinate):
    	delta_width = 100
    	delta_height = 100
    	y = 50
    	#current_symbols = self.symbols_coordinate[current_symbols]
    	for i in range( len(coordinate) ):
    		self.plate_image = self.create_image(image, coordinate[i])
    		size = (0.3 * self.width, 0.1 * self.width)
    		self.resized = self.plate_image.resize( (int(size[0]), int(size[1])), Image.ANTIALIAS )
        	self.photo_plate = ImageTk.PhotoImage( self.resized )
        	self.canvas.create_image( int(self.viewer_scale[0] * self.width) + 50, y,
        							 anchor = "nw", image = self.photo_plate, tags = 'image' )
        	#draw_framing(plate_image, current_symbols[i])
    		    	     

	def draw_framing(self, image, coordinate):
		for coord in coordinate:
			canvas.create_rectangle(coordinate[0], coordinate[1], 
									coordinate[0] + coordinate[2],
									coordinate[1] + coordinate[3],
									outline='red', width=2)		

    def skip(self, event):
    	self.rect = None
    	self.current_index += 1
    	self.draw_image()

    def create_image(self, pix, coordinates):
		start_x = coordinates[0]
		start_y = coordinates[1]
		width = coordinates[2]
		height = coordinates[3]
		new_image = Image.new( 'RGB', (width, height) )
		draw = ImageDraw.Draw(new_image)
		for w in range(width):
			for h in range(height):
				draw.point( (w, h), pix[start_x + w, start_y + h] )
		return new_image



def search_plate(image, cascades):
	plates = np.empty((0, 4), dtype = int)
	for cascade in cascades:
		obj = cascade.detectMultiScale( image, scaleFactor=1.1, minNeighbors=5 )
		if len(obj) != 0: 
			plates = np.append(plates, obj, axis = 0)
			'''
			for (x, y, w, h) in obj:
					cv2.imshow("", image[y: y + h, x: x + w])
					cv2.waitKey(0)
			'''			
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
	width_newimg = 50
	height_newimg = 70
	start_x = coordinates[0]
	start_y = coordinates[1]
	width = coordinates[2]
	height = coordinates[3]
	if width > width_newimg:
		width = width_newimg
	if height > height_newimg:
		height = height_newimg
	delta_width = (width_newimg - width) / 2
	delta_height = (height_newimg - height) / 2
	new_image = Image.new( 'L', (width_newimg, height_newimg), 255 )
	draw = ImageDraw.Draw(new_image)
	for w in range(width):
		for h in range(height):
			draw.point( (w + delta_width, h + delta_height),
						int(pix[start_y + h][start_x + w]) )
	return new_image

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

def symbols_from_nn(pix_image, symbols):
	model = create_nn_model( "nn_model.json", "nn_model.h5" )
	nn_symbols = {}
	for key, values in symbols.items():
		for coordinate in values:
			symbols_image = create_50_70_image(pix_image, coordinate)
			#symbols_image.show()
			pix = image.img_to_array(symbols_image)
			pix = np.expand_dims(pix, axis = 0)
			preds = model.predict(pix)
			label = np.argmax(preds)
			#print("coordinate: {}".format(coordinate))
			#print("key: {}".format(key))
			#print("label: {}".format(label))
			if label not in nn_symbols:
				nn_symbols[label] = np.array([coordinate])
			else:
				nn_symbols[label] = np.append(nn_symbols[label], [coordinate], axis = 0)
	return nn_symbols

'''
def symbols_from_nn(pix_image, symbols):
	model = create_nn_model( "nn_model.json", "nn_model.h5" )
	nn_symbols = {}
	for key, values in symbols.items():
		for coordinate in values:
			symbols_image = create_50_70_image(pix_image, coordinate)
			#symbols_image.show()
			pix = image.img_to_array(symbols_image)
			pix = np.expand_dims(pix, axis = 0)
			preds = model.predict(pix)
			label = np.argmax(preds)
			if label not in nn_symbols:
				nn_symbols[label] = np.array([coordinate])
			else:
				nn_symbols[label] = np.append(nn_symbols[label], [coordinate], axis = 0)
	return nn_symbols
'''
def mutual_square(coordinate_1, coordinate_2):
	x1 = max( coordinate_1[0], coordinate_2[0] )
	y1 = max( coordinate_1[1], coordinate_2[1] )
	x2 = min( coordinate_1[0] + coordinate_1[2],
			coordinate_2[0] + coordinate_2[2] )
	y2 = min( coordinate_1[1] + coordinate_1[3], 
			coordinate_2[1] + coordinate_2[3] )
	return (x2 - x1) * (y2 - y1)

def intersection_area(coordinate_1, coordinate_2):
	square_1 = coordinate_1[2] * coordinate_1[3]
	square_2 = coordinate_2[2] * coordinate_2[3]
	mut_sq = mutual_square(coordinate_1, coordinate_2)
	return mut_sq / (square_1 + square_2 - mut_sq)


def print_number(pix, x_0, y_0, widthImg, heightImg):
    newImg=Image.new('L', (widthImg, heightImg))
    draw = ImageDraw.Draw(newImg)
    for w in range(widthImg):
        for h in range(heightImg):
            draw.point((w, h), (pix[y_0 + h, x_0 + w]))
    newImg.show();

def main():
	file_with_photo = sys.argv[1]
	report_file_name = sys.argv[2]

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

	all_photo = []
	photo_plates = []
	photos_list = [name.replace('\n', '') for name in open( file_with_photo, 'r' )]
	for obj in photos_list:
		image = Image.open(obj).convert('L')
		full_image_arr = np.array( image )	

		plates = search_plate( full_image_arr, plate_cascade )
		photo_plates.append(plates)

		cascade_symbols = {}
		nn_symbols = {}

		for i in range( len(plates) ):
			plate_image = get_pixels_image( full_image_arr, plates[i] )
			plate_img = create_new_image( image.load(), plates[i] )
			plate_img.show()
			cascade_symbols[i] = search_symbols( plate_image, symbols_cascade_dict )
			nn_symbols[i] = symbols_from_nn(plate_image, cascade_symbols[i])
			
			for key in sorted(cascade_symbols[i].keys()):
				print("cascades: {} -> {}".format(key, cascade_symbols[i][key]))

			for key in sorted(nn_symbols[i].keys()):
				print("nn: {} -> {}".format(key, nn_symbols[i][key]))
			all_photo.append(nn_symbols[i])


		for i in range( len(plates) ):		
			for key in sorted(cascade_symbols[i].keys()):
				plate_img = create_new_image( image.load(), plates[i] )
				pix = plate_img.load()
				for coordinates in cascade_symbols[i][key]:
					img = create_new_image(pix, coordinates)	
					#img.show()
				

		
	#print(all_photo)
	app = ExampleApp(file_with_photo, photo_plates, all_photo, report_file_name)
	app.mainloop()

if __name__ == '__main__':
    main()