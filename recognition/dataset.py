#!/usr/bin/env python3

import os
import sys
from PIL import Image, ImageDraw 
import numpy as np

def pix_to_arr(pix, height, width):
	matrix = np.empty( (height, width, 1) )
	for h in range (height):
		for w in range (width):
			matrix[h][w] = pix[w, h] 
	return matrix

def new_image(pix, height_img, width_img, height_newimg, width_newimg):
	new_img=Image.new('L', (width_newimg, height_newimg), 255)
	draw = ImageDraw.Draw(new_img)
	delta_width = (width_newimg - width_img) / 2
	delta_height = (height_newimg - height_img) / 2
	for i in range(height_img):
		for j in range(width_img):
			draw.point((j + delta_width, i + delta_height), pix[j, i])
	return new_img


def load_training(path = '/home/alexander/projects/alex_alex/car-license-plate-recognition/datasets/datasets_symbols/train_image.txt'):
	file = open (path, 'r')	
	arr_lines = file.readlines()
	number_img = len(arr_lines)
	arr_image = np.empty((number_img, 50, 70, 1)) #!!!
	arr_labels = np.empty(number_img)
	i = 0
	for line in arr_lines:
		path_image, labels = line.split(' ')
		image = Image.open(path_image).convert('L')
		image = new_image(image.load(), image.size[1], image.size[0], 50, 70)
		pixels = pix_to_arr ( image.load(), image.size[1], image.size[0] )
		arr_image[i] = pixels
		arr_labels[i] = int(labels)
		i += 1
	file.close()
	return arr_image, arr_labels


def load_testing(path = '/home/alexander/projects/alex_alex/car-license-plate-recognition/datasets/datasets_symbols/test_image.txt'):
	file = open (path, 'r')	
	arr_lines = file.readlines()
	number_img = len(arr_lines)
	arr_image = np.empty((number_img, 50, 70, 1)) #!!!
	arr_labels = np.empty(number_img)
	i = 0
	for line in arr_lines:
		path_image, labels = line.split(' ')
		image = Image.open(path_image).convert('L')
		image = new_image(image.load(), image.size[1], image.size[0], 50, 70)
		pixels = pix_to_arr ( image.load(), image.size[1], image.size[0] )
		arr_image[i] = pixels
		arr_labels[i] = int(labels)
		i += 1
	file.close()
	return arr_image, arr_labels


def main():
	training_image, training_labels = load_training()
	testing_image, testing_labels = load_testing()

if __name__ == '__main__':
	main()