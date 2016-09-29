#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter as tk
import tkFileDialog
import os
from histogram_window import histogram_window
from PIL import ImageTk, Image
import subprocess
import platform
from image_processing import image_processing



class ApplicationView:
    def __init__(self):
        pass

    def initialize(self,app):
        self.root = app
        self.histogram_window = None
        self.imageFrame = tk.Frame(app,background="red")
        self.imageFrame.pack(side = "left",fill = "both", expand = "True")

        self.buttonsFrame = tk.Frame(app, width = 0)
        self.buttonsFrame.pack(side = "right",fill = "y")

        self.image_path = '/Users/alex/Downloads/unspecified1.jpeg'
        self.imageLabel = tk.Label(self.imageFrame)
        self.imageLabel.pack(fill = "both", expand = "True")
        self.imageLabel.bind('<Configure>', self.resize_image)
        self.change_image(Image.open(self.image_path))

        buttons_width = 12

        load_image_button = tk.Button(self.buttonsFrame , text="Load image", width = buttons_width, command = self.load_image)
        load_image_button.pack( side = "top", padx = 5, pady = 10)

        show_histogram_button = tk.Button(self.buttonsFrame , text="Show histogram", width = buttons_width, command = self.show_histogram)
        show_histogram_button.pack( side = "top", padx = 5, pady = 10)

        greyscale_button = tk.Button(self.buttonsFrame , text="Apply greyscale", width = buttons_width, command = self.apply_greyscale)
        greyscale_button.pack( side = "top", padx = 5, pady = 10)

        self.create_prepare_views(buttons_width)


        self.file_opt = options = {}
        options['defaultextension'] = '.jpg'
        options['filetypes'] = [('image files', ('.jpeg','.jpg','.JPG','.JPEG'))]
        options['initialdir'] = os.path.expanduser('~')
        options['initialfile'] = 'myfile.txt'
        options['parent'] = app.root
        options['title'] = 'Choose file'

    def create_prepare_views(self,width):
        self.gmin_string = tk.StringVar()
        self.gmax_string = tk.StringVar()
        self.create_prepare_view(width,1,self.apply_prepare1,"gmin","gmax",self.gmin_string,self.gmax_string)

        self.fmin_string = tk.StringVar()
        self.fmax_string = tk.StringVar()
        self.create_prepare_view(width,2,self.apply_prepare2,"fmin","fmax",self.fmin_string,self.fmax_string)

    def create_prepare_view(self, buttons_width, number,command,name_min,name_max,min_stringvar,max_stringvar):
        prepare_frame = tk.Frame(self.buttonsFrame)
        prepare_frame.pack( side = "top", padx = 5, pady = 8)

        prepare_button = tk.Button(prepare_frame , text="Prepare "+str(number), width = buttons_width, command = command)
        prepare_button.pack( side = "top", padx = 5, pady = 3)

        min_frame = tk.Frame(prepare_frame)
        min_frame.pack( side = "top", padx = 5, pady = 2)

        min_label = tk.Label(min_frame, text = name_min, width = 10)
        min_label.pack(side = "left")

        min_field = tk.Entry(min_frame, textvariable=min_stringvar,width = 6)
        min_field.pack( side = "right",padx = 8)
        min_field.bind("<Button-1>", self.click_on_field)
        min_stringvar.set(name_min)

        max_frame = tk.Frame(prepare_frame)
        max_frame.pack( side = "top", padx = 5, pady = 2)

        max_label = tk.Label(max_frame, text = name_max, width = 10)
        max_label.pack(side = "left")

        max_field = tk.Entry(max_frame, textvariable=max_stringvar,width = 6)
        max_field.pack( side = "right",padx = 8)
        max_field.bind("<Button-1>", self.click_on_field)
        max_stringvar.set(name_max)

    def load_image(self):
        image_file = tkFileDialog.askopenfile(**self.file_opt)
        self.image_file = image_file.name
        self.change_image(Image.open(image_file))
        self.resize_image((0,0))

    def show_histogram(self):
        self.histogram_window = histogram_window(self.image,self.image_path)

    def apply_greyscale(self):
        gray_image = image_processing.greyscale(self.imagecopy)
        self.change_image(gray_image)
        self.resize_image((0,0))

    def apply_prepare1(self):
        print self.gmin_string.get()
        prepare = image_processing.prepare1(image=self.imagecopy, gmin=int(self.gmin_string.get()), gmax=int(self.gmax_string.get()))
        self.change_image(prepare)
        self.resize_image((0,0))

    def apply_prepare2(self):
        prepare = image_processing.prepare2(self.imagecopy)
        self.change_image(prepare)
        self.resize_image((0,0))

    def change_image(self, new_image):
        self.image = new_image
        self.imagecopy = self.image.copy()
        self.update_label_image(self.image)

    def update_label_image(self, new_image):
        img = ImageTk.PhotoImage(new_image)
        self.imageLabel.configure(image = img)
        self.imageLabel.image = img

    def click_on_field(self, event):
        event.widget.selection_range(0, tk.END)

    def resize_image(self,event):
        width, height = self.image.size
        fwidth = self.root.winfo_width()-150
        fheight = self.imageLabel.winfo_height()
        ratiow = fwidth / float(width)
        ratiof = fheight / float(height)
        ratio = min(ratiow, ratiof)
        self.image = self.imagecopy.resize((int(width*ratio), int(height*ratio)))
        self.update_label_image(self.image)
