#!/usr/bin/env python

import os
import sys


def rename_image(path):
	listOfFiles = os.listdir(path)
	countOfFiles = len(listOfFiles)
	for i in range (0, countOfFiles):
		os.rename(path+ '/' + listOfFiles[i], path + '/' + '_' +  str(i) + '.bmp')

def main():
	path = sys.argv[1]
	for obj in os.listdir(path): 
		obj = os.path.join(path, obj)
		rename_image(obj)


if __name__ == '__main__':
    main()
