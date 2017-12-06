#!/usr/bin/env python3

import os
import sys
from PIL import Image, ImageDraw 

def new_image(pix, width_img, height_img, width_newimg, height_newimg):
	new_img=Image.new('L', (width_newimg, height_newimg), 255)
	draw = ImageDraw.Draw(new_img)
	delta_width = (width_newimg - width_img) / 2
	delta_height = (height_newimg - height_img) / 2
	for i in range(height_img):
		for j in range(width_img):
			draw.point((j + delta_width, i + delta_height), pix[j, i])
	return new_img

def main():
	path = sys.argv[1]
	image1 = Image.open(path)
	image1.show()
	image2 = new_image(image1.load(), image1.size[0], image1.size[1], 50, 70)
	image2.show()


if __name__ == '__main__':
	main()