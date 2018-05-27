#!/usr/bin/env python

import os
import sys
import random

def create_file(path, number_photo, report):
    img_extension = ['jpg', 'jpeg', 'bmp', 'png']
    report = open(report, 'w')
   
    print number_photo , len(os.listdir(path))


    if number_photo > len(os.listdir(path)):
        number_photo = len(os.listdir(path))

    print number_photo

    for name in random.sample(os.listdir(path), number_photo):
        report.write(os.path.abspath(os.path.join(path, name)) + "\n")

    report.close()
    return


def main():
    try:
        path_to_photo = sys.argv[1]
    except Exception as e:
        print "Expected path to directory with images"
        return

    number_photo = int(sys.argv[2])

    report = sys.argv[3]
    
    create_file(path_to_photo, number_photo, report)
    

if __name__ == '__main__':
    main()