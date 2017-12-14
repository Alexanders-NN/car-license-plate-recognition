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
	all_img = []
	bad_size = 1500
	if os.path.isfile(path):
		all_img += read_file(path)
	shuffle(all_img)
	if len(all_img) < 1500:
		bad_size = len(all_img) 
	new_bad_file = open(path, 'w')
	for i in range( bad_size ):
		new_bad_file.write( all_img[i] )
	new_bad_file.close()


if __name__ == '__main__':
    main()