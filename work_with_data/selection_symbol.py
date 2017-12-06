#!/usr/bin/env python

import os
import sys
from PIL import Image

def size(filepath):
    s = (0, 0)
    with Image.open(filepath) as img:
        s = img.size
    return s

def entry_in_file(path, path_for_entry):
	max_width = 50
	max_height = 70
	labels = path.split('/')[-1]
	format = ".txt"
	path_for_entry = path_for_entry + '/' + labels
	result = []
	file = open(path_for_entry, 'w')
	for img in os.listdir(path):
		img = os.path.join(path, img)
		size_img = size(img) 
		if size_img[0] <= max_width and size_img[1] <= max_height:

			file.write(os.path.abspath(img) + ' ' + labels + '\n')
	file.close()
	return


def main():
	path = sys.argv[1]
	rez_path = sys.argv[2]
	for obj in os.listdir(path): 
		obj = os.path.join(path, obj)
		entry_in_file(obj, rez_path)


if __name__ == '__main__':
    main()
