#!/usr/bin/python3

import numpy
import dataset
from keras import Sequential
from keras.utils import np_utils 
from keras.models import model_from_json

json_file = open( "model_1.json" )
loaded_model = json_file.read()
json_file.close()

model = model_from_json(loaded_model)

model.load_weights ("model1.h5")

testing_images, testing_labels = dataset.load_testing()

testing_images = testing_images.astype('float32')
testing_images /= 255

testing_labels = np_utils.to_categorical(testing_labels, 21)

model.compile( loss = 'categorical_crossentropy', optimizer = 'SGD',
			metrics = ['accuracy'] )

scores = model.evaluate(testing_images, testing_labels, verbose=0)

print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))