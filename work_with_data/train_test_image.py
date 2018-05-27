#!/usr/bin/python3

import os
import sys
from PIL import Image
from random import shuffle

def size(filepath):
    s = (0, 0)
    with Image.open(filepath) as img:
        s = img.size
    return s

def get_image(path):
	max_width = 50
	max_height = 70
	labels = path.split('/')[-1]
	format = ".txt"
	result = []
	for img in os.listdir(path):
		img = os.path.join(path, img)
		size_img = size(img) 
		if size_img[0] <= max_width and size_img[1] <= max_height:
			str = os.path.abspath(img) + ' ' + labels + '\n'
			result.append(str)
	return result


def main():
	path = sys.argv[1]
	rez_parh = sys.argv[2]
	
	train_path = rez_parh + '/train_image.txt'
	test_path = rez_parh + '/test_image.txt'
	train_file = open(train_path, 'w')
	test_file = open(test_path, 'w')

	all_img = []
	k = 0.85


	for obj in os.listdir(path): 
		obj = os.path.join(path, obj)
		all_img += get_image(obj)


	shuffle(all_img)
	train_size = len(all_img) * k
	round(train_size)
	for i in range( len(all_img) ):
		if i <= train_size:
			train_file.write(all_img[i])
		else:
			test_file.write(all_img[i])
	train_file.close()
	test_file.close()

if __name__ == '__main__':
	main()