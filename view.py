#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter as tk
import tkFileDialog
import os
from histogram_window import histogram_window
from PIL import ImageTk, Image
import subprocess
import platform

class ApplicationView:
    def __init__(self):
        pass

    def initialize(self,app):
        self.root = app
        self.histogram_window = None
        self.imageFrame = tk.Frame(app,background="red")
        self.imageFrame.pack(side = "left",fill = "both", expand = "True")

        self.buttonsFrame = tk.Frame(app, width = 100)
        self.buttonsFrame.pack(side = "right",fill = "y")

        self.image_path = '/Users/alex/Downloads/unspecified1.jpeg'
        self.image = Image.open(self.image_path);
        self.imagecopy = self.image.copy()
        img = ImageTk.PhotoImage(self.image)
        self.imageLabel = tk.Label(self.imageFrame, image = img)
        self.imageLabel.image = img
        self.imageLabel.pack(fill = "both", expand = "True")
        self.imageLabel.bind('<Configure>', self.resize_image)

        load_image_button = tk.Button(self.buttonsFrame , text="Load image", fg="red", command = self.load_image)
        load_image_button.pack( side = "top", padx = 10, pady = 10)

        show_histogram_button = tk.Button(self.buttonsFrame , text="Show histogram", fg="red", command = self.show_histogram)
        show_histogram_button.pack( side = "top", padx = 10, pady = 10)

        self.file_opt = options = {}
        options['defaultextension'] = '.jpg'
        options['filetypes'] = [('image files', ('.jpeg','.jpg','.JPG','.JPEG','.png','.PNG'))]
        options['initialdir'] = os.path.expanduser('~')
        options['initialfile'] = 'myfile.txt'
        options['parent'] = app.root
        options['title'] = 'Choose file'

    def load_image(self):
        self.image_path = tkFileDialog.askopenfile(**self.file_opt)
        self.image = Image.open(self.image_path);
        self.imagecopy = self.image.copy()
        img = ImageTk.PhotoImage(self.image)
        self.imageLabel.configure(image = img)
        self.imageLabel.image = img
        self.resize_image((0,0))

    def show_histogram(self):
            self.histogram_window = histogram_window(self.image,self.image_path)

    def resize_image(self,event):
        width, height = self.image.size
        fwidth = self.root.winfo_width()-120
        fheight = self.imageLabel.winfo_height()

        ratiow = fwidth/float(width)
        ratiof = fheight/float(height)
        ratio = min(ratiow,ratiof)

        self.image = self.imagecopy.resize((int(width*ratio), int(height*ratio)))
        photo = ImageTk.PhotoImage(self.image)
        self.imageLabel.config(image = photo)
        self.imageLabel.image = photo #avoid garbage collection
