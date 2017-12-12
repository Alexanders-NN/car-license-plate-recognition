#!/usr/bin/env python

import os
import sys

from collections import defaultdict
from PIL import Image
from random import randint


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

def create_good_file(path, path_for_entry):
    img_extension = ['jpg', 'jpeg', 'bmp', 'png']
    labels = path.split('/')[-1]
    format = ".dat"
    path_for_entry = path_for_entry + '/' + 'good' + '_' + labels + format
    file = open(path_for_entry, 'w')

    images = []
    for obj in os.listdir(path):
        obj = os.path.join(path, obj)
        if os.path.isfile(obj) and obj.split('.')[-1] in img_extension:
            images.append(( obj, get_size(obj) ))

    for name, size in images:
        file.write( "{} 1 0 0 {} {}\n".format(os.path.abspath(name), size[0], size[1]) )
    file.close()
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


def create_bad_file(path, path_for_entry, number_file):
    format = ".dat"
    path_for_entry = path_for_entry + '/' + 'bad' + '_' + str(number_file) + format
    file = open(path_for_entry, 'w')
    data = []

    for obj in os.listdir(path):
    	persent = 0.1
        if int(obj) == number_file:
            continue
        elif int(obj) == 21:
            persent = 1
        obj = os.path.join( path, obj )
        data += get_bad_data( obj, persent )

    for name in data:
        file.write( "{}\n".format(os.path.abspath(name)) )
    file.close()
    return


def main():
    try:
        path = sys.argv[1]
    except Exception as e:
        print "Expected path to directory with images"
        return

    try:
        good_report = sys.argv[2]
    except Exception as e:
        print "Expected path to directory for good data"
        return

    try:
        bad_report = sys.argv[3]
    except Exception as e:
        print "Expected path to directory for bad data"
        

    for obj in os.listdir(path):
    	obj = os.path.join(path, obj)
    	create_good_file(obj, good_report)

    for i in range(21):
        create_bad_file(path, bad_report, i)
    

if __name__ == '__main__':
    main()