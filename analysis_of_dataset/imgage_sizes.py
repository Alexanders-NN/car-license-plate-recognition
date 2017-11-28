#!/usr/bin/env python

import os
import sys
from collections import defaultdict

from PIL import Image

try:
    import Tkinter as tk

except:
    print "I can't find module 'Tkinter'. Try this:"
    print "    sudo apt-get install python-tk python3-tk"



class ShowStatistics(tk.Tk):

    def __init__(self, size_statistic, report):
        tk.Tk.__init__(self)

        size = (self.winfo_screenwidth() * 0.8, 
            self.winfo_screenheight() * 0.8)

        self.statistics = size_statistic
        self.report = open(report, 'w')


        self.canvas = tk.Canvas(self, width=size[0], height=size[1], cursor="cross", bg="lightblue")
        self.canvas.pack(side="top", fill="both", expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        #self.canvas.bind("<B1-Motion>", self.on_move_press)
        #self.canvas.bind("<Motion>", self.on_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        #self.bind("<Tab>", self.save)
        #self.bind("<Key>", self.key)

        self.draw_image()


    def draw_image(self):
       
        self.X_line = self.canvas.create_line(0,0,0,0,fill='red',width=2,dash=(5,3), tags='x-line')
        self.Y_line = self.canvas.create_line(0,0,0,0,fill='red',width=2,dash=(5,3), tags='y-line')

        for size in self.statistics:
            python_green = "#476042"
            x, y = size
            x1, y1 = (x - 1, y - 1)
            x2, y2 = (x + 1, y + 1)
            self.canvas.create_oval(x1, y1, x2, y2, fill=python_green)

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        #one rectangle
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, tags='rect')

    def on_move(self, event):
        curX, curY = event.x, event.y
        self.canvas.coords(self.X_line, curX, 0, curX, self.height)
        self.canvas.coords(self.Y_line, 0, curY, self.width, curY)

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)
        

    def on_button_release(self, event):
        self.end_x, self.end_y = (event.x, event.y)


    def __del__(self):
        close(self.report)


"""if __name__ == "__main__":
    path_to_photos = fix_path(sys.argv[1])
    report_file_name = fix_path(sys.argv[2])
    app = ExampleApp(path_to_photos, report_file_name)
    app.mainloop()
    """

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

    statistics = counter()
    maximum_size = (0, 0)
    for name, size in image_sizes(path):
        statistics[size] += 1
        if size[0] > maximum_size[0]:
            maximum_size = (size[0], maximum_size[1])
        if size[1] > maximum_size[1]:
            maximum_size = (maximum_size[0], size[1])

    for size in sorted(statistics.keys()):
    	if statistics[size] > 50:
        	print "{} : {}".format(size, statistics[size])

    print "max sizes = {}".format(maximum_size)

    app = ShowStatistics(statistics, report)
    app.mainloop()





if __name__ == '__main__':
	main()


