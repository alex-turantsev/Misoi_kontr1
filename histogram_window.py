#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter as tk
from PIL import ImageTk, Image

class histogram_window(tk.Tk):
    def __init__(self,image):
        tk.Tk.__init__(self)
        self.root = self

        self.title('Histogram')
        self.geometry('500x350');
        self.minsize(500, 350)
        self.maxsize(500, 350)

        self.draw_histogram()

        self.mainloop()

    

    def draw_histogram(self):
        data = [20, 15, 10, 7, 5, 4, 3, 2, 4, 21, 0,15,5,3,7,9,3,1,7,8,4,0,2,4,7,2]
        c_width = 500                                                       # Define it's width
        c_height = 350                                                      # Define it's height
        c = tk.Canvas(self, width=c_width, height=c_height, bg= 'white')    # Create a canvas and use the earlier dimensions
        c.pack()
        y_stretch = 15                                                      # The highest y = max_data_value * y_stretch
        y_gap = 20                                                          # The gap between lower canvas edge and x axis
        x_stretch = 5                                                      # Stretch x wide enough to fit the variables
        x_width = 2                                                        # The width of the x-axis
        x_gap = 20                                                          # The gap between left canvas edge and y axis
        for x, y in enumerate(data):                                        # A quick for loop to calculate the rectangle
                                                                            # coordinates of each bar
            x0 = x * x_stretch + x * x_width + x_gap                        # Bottom left coordinate
            y0 = c_height - (y * y_stretch + y_gap)                         # Top left coordinates
            x1 = x * x_stretch + x * x_width + x_width + x_gap              # Bottom right coordinates
            y1 = c_height - y_gap                                           # Top right coordinates
            c.create_rectangle(x0, y0, x1, y1, fill="grey", outline="grey")                  # Draw the bar
            #c.create_text(x0+2, y0, anchor=tk.SW, text=str(y))              # Put the y value above the bar
