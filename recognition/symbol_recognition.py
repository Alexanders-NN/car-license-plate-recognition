#!/usr/bin/python3

import numpy
from keras.datasets import mnist, cifar10
from keras import Sequential
from keras.layers import Dense, Flatten, Activation, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.utils import np_utils 
import dataset

numpy.random.seed(42)

training_images, training_labels = dataset.load_training()
testing_images, testing_labels = dataset.load_testing()

training_images = training_images.astype('float32')
testing_images = testing_images.astype('float32')
training_images /= 255
testing_images /= 255

training_labels = np_utils.to_categorical(training_labels, 21)
testing_labels = np_utils.to_categorical(testing_labels, 21)

model = Sequential()
'''
model.add( Convolution2D(16, (3, 3), input_shape = (50, 70, 1), 
			padding = 'same', data_format = 'channels_last',
			activation = 'relu', use_bias = True) )

model.add( Convolution2D(16, (3, 3), padding = 'same', 
			data_format = 'channels_last',	activation = 'relu', 
			use_bias = True) )

model.add( MaxPooling2D ( pool_size = (2, 2), 
			data_format = 'channels_last' ) )

model.add ( Dropout(0.25) )

model.add( Convolution2D(32, (3, 3), padding = 'same', 
			data_format = 'channels_last',	activation = 'relu', 
			use_bias = True) )

model.add( Convolution2D(64, (3, 3), padding = 'same', 
			data_format = 'channels_last',	activation = 'relu', 
			use_bias = True) )

model.add( MaxPooling2D ( pool_size = (2, 2), 
			data_format = 'channels_last' ) )

model.add( Dropout(0.25) )

model.add( Flatten() )

model.add( Dense(1024, activation = 'relu', use_bias = True) )

model.add( Dropout(0.25) )
'''
model.add(Convolution2D(75, kernel_size=(5, 5),
                 activation='relu',
                 input_shape=(50, 70, 1)))

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Dropout(0.2))

model.add(Convolution2D(100, (5, 5), activation='relu'))

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Dropout(0.2))

model.add(Flatten())

model.add(Dense(500, activation='relu'))

model.add(Dropout(0.5))

model.add( Dense(21, activation = 'relu', use_bias = True) )

model.add(Activation('softmax'))

model.compile( loss = 'categorical_crossentropy', optimizer = 'SGD',
			metrics = ['accuracy'] )

model.fit( training_images, training_labels, batch_size = 100,
			epochs = 10, validation_split = 0.15)


model_json = model.to_json()
json_file = open("model_1.json", "w")
json_file.write(model_json)
json_file.close()

model.save_weights("model1.h5py")

#print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))