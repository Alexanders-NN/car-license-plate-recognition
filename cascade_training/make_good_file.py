#!/usr/bin/env python

import os
import sys

from collections import defaultdict
from PIL import Image


def counter():
    return defaultdict(lambda: 0)

def size(filepath):
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
            result.append((obj, size(obj) ))
        elif os.path.isdir(obj):
            result += image_sizes(obj)

    return result


def main():
    path = './'
    report = 'REPORT'
    try:
        path = sys.argv[1]
    except Exception as e:
        print "Expected path to directory with images"
        return

    try:
        report = sys.argv[2]
    except Exception as e:
        print "Expected report name"
        return

    file = open(report, 'w')
    for name, size in image_sizes(path):
        file.write( "{} 1 0 0 {} {}\n".format(name, size[0], size[1]) )



if __name__ == '__main__':
    main()



