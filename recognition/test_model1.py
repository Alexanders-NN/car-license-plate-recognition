#!/usr/bin/python3

import cv2, os, sys
from PIL import Image, ImageDraw
import numpy as np
import dataset
from keras import Sequential
from keras.utils import np_utils 
from keras.models import model_from_json
from keras.preprocessing import image

json_file = open( "nn_model.json" )
loaded_model = json_file.read()
json_file.close()

model = model_from_json(loaded_model)
model.load_weights ("nn_model.h5")

testing_images, testing_labels = dataset.load_testing()

testing_images = testing_images.astype('float32')
testing_images /= 255

testing_labels = np_utils.to_categorical(testing_labels, 21)

model.compile( loss = 'categorical_crossentropy', optimizer = 'SGD',
			metrics = ['accuracy'] )

scores = model.evaluate(testing_images, testing_labels, verbose=0)

print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))

'''
def main():
	path_to_photo = sys.argv[1]
	
	json_file = open( "nn_model.json" )
	loaded_model = json_file.read()
	json_file.close()

	model = model_from_json(loaded_model)
	#model.load_weights ("weights/epoch_9.h5")
	model.load_weights ("nn_model.h5")
	
	symbols = []
	i=0
	for obj in os.listdir(path_to_photo):
		if i < 21:
			obj = os.path.join(path_to_photo, obj)
			print(obj)
			img = image.load_img( obj, target_size = (70, 50), grayscale=True )
			#img.show()
			x = image.img_to_array(img)
			#x = np.array(img)
			x = np.expand_dims(x, axis = 0)
			preds = model.predict(x)
			symbols.append( np.argmax(preds) )
			i = i + 1
		else:
			break
	print('Результаты распознования', symbols)



if __name__ == '__main__':
	main()
'''