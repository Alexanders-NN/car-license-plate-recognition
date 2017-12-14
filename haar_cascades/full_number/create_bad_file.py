#!/usr/bin/env python

import sys
import os

def main():
	path_to_photo = sys.argv[1]
	result_path = sys.argv[2]
	file = open(result_path, 'w')
	for img in os.listdir( path_to_photo ):
		img = os.path.join( path_to_photo, img )
		file.write( "{}\n".format( os.path.abspath(img) ) )
	file.close()

if __name__ == '__main__':
	main()