#!/usr/bin/python3

import os
import sys
from random import shuffle

def read_file(path):
	file = open(path, 'r')
	result = []
	for line in file.readlines():
		result.append(line)
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
		if os.path.isfile(obj):
			all_img += read_file(obj)
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