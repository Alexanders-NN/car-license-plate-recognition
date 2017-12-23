#!/usr/bin/env python

import os
import sys

from collections import defaultdict
from PIL import Image
from random import randint, shuffle


def get_size(filepath):
    s = (0, 0)
    with Image.open(filepath) as img:
        s = img.size
    return s


def image_sizes(path):
    img_extension = ['jpg', 'jpeg', 'bmp', 'png']
    result = []
    for obj in os.listdir(path):
        obj = os.path.join(path, obj)
        if os.path.isfile(obj) and obj.split('.')[-1] in img_extension:
            result.append((obj, get_size(obj) ))
        elif os.path.isdir(obj):
            result += image_sizes(obj)
    return result

def get_good_data(path):
    img_extension = ['jpg', 'jpeg', 'bmp', 'png']
    result = []
    for img in os.listdir(path):
        img = os.path.join( path, img )
        if os.path.isfile(img) and img.split('.')[-1] in img_extension:
            result.append(img)
    return result

def create_good_file(path, path_for_numbers, path_for_letters):
    
    format = ".dat"
    path_for_numbers = path_for_numbers + '/' + 'good' + format
    path_for_letters = path_for_letters + '/' + 'good' + format
    numbers_file = open(path_for_numbers, 'w')
    letters_file = open(path_for_letters, 'w')

    numbers_images = []
    letters_images = []

    for obj in os.listdir(path):
        labels = int(obj) 
        obj = os.path.join(path, obj)
        if labels <= 9:
            print(1)
            numbers_images += get_good_data(obj)
        elif labels != 21:
            print(2)
            letters_images += get_good_data(obj)

    shuffle(numbers_images)
    shuffle(letters_images)  

    for name in numbers_images:
        size = get_size(name)
        numbers_file.write( "{} 1 0 0 {} {}\n".format( os.path.abspath(name), size[0], size[1] ) )

    for name in letters_images:
        size = get_size(name)
        letters_file.write( "{} 1 0 0 {} {}\n".format( os.path.abspath(name), size[0], size[1] ) )

    numbers_file.close()
    letters_file.close()
    return

def get_bad_data(path, persent):
    img_extension = ['jpg', 'jpeg', 'bmp', 'png']
    result = []    
    number = persent * len( os.listdir(path) ) 
    round(number)
    i = 0
    for obj in os.listdir(path):
        if i >= number:
            break
        obj = os.path.join(path, obj)
        if os.path.isfile(obj) and obj.split('.')[-1] in img_extension:
            result.append(obj)
        i += 1
    return result


def create_bad_file(path, path_for_numbers, path_for_letters):
    format = ".dat"
    path_for_numbers = path_for_numbers + '/' + 'bad' + format
    path_for_letters = path_for_letters + '/' + 'bad' + format
    numbers_file = open(path_for_numbers, 'w')
    letters_file = open(path_for_letters, 'w')
    numbers_images = []
    letters_images = []
    
    for obj in os.listdir(path):
        persent = 0.1
        labels = int(obj)
        if labels == 21:
            persent = 1
        obj = os.path.join( path, obj )
        if labels <= 9 or labels == 21:
            print(3)
            letters_images += get_bad_data( obj, persent )
        if labels > 9:
            print(4)
            numbers_images += get_bad_data(obj, persent)

    shuffle(numbers_images)
    shuffle(letters_images)

    for name in numbers_images:
        numbers_file.write( "{}\n".format(os.path.abspath(name)) )
    for name in letters_images:
        letters_file.write( "{}\n".format(os.path.abspath(name)) )

    numbers_file.close()
    letters_file.close()
    return


def main():
    try:
        path = sys.argv[1]
    except Exception as e:
        print "Expected path to directory with images"
        return

    try:
        numbers_report = sys.argv[2]
    except Exception as e:
        print "Expected path to directory for numbers"
        return

    try:
        letters_report = sys.argv[3]
    except Exception as e:
        print "Expected path to directory for letters"
        
    create_good_file( path, numbers_report, letters_report )
    create_bad_file( path, numbers_report, letters_report )
    

if __name__ == '__main__':
    main()