#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter as tk
import tkFileDialog
import os
import os.path
from histogram_window import histogram_window
from PIL import ImageTk, Image
import subprocess
import platform
from image_processing import image_processing
from operator_filter import *
import ntpath

class ApplicationView:
    def __init__(self):
        pass

    def initialize(self,app):
        self.root = app
        self.histogram_window = None
        self.imageFrame = tk.Frame(app, bg="red")
        self.imageFrame.pack(side = "left", fill = "both", expand = "True")

        self.buttonsFrame = tk.Frame(app, width = 0)
        self.buttonsFrame.pack(side = "right",fill = "y")

        self.image_path = '/Users/alex/Downloads/unspecified1.jpeg'
        self.imageLabel = tk.Label(self.imageFrame)
        self.imageLabel.pack(fill = "both", expand = "True")
        self.imageLabel.bind('<Configure>', self.resize_image)
        try:
            self.change_image(Image.open(self.image_path))
        except:
            pass
        self.create_left_buttons()

        self.file_opt = options = {}
        options['defaultextension'] = '.jpg'
        options['filetypes'] = [('image files', ('.jpeg','.jpg','.JPG','.JPEG','.png','.PNG'))]
        options['initialdir'] = os.path.expanduser('~')
        options['initialfile'] = 'myfile.jpg'
        options['parent'] = app.root
        options['title'] = 'Choose file'

    def create_left_buttons(self):
        buttons_width = 12

        self.create_button(parent=self.buttonsFrame,text="Load image",width=buttons_width,command=self.load_image_with_ask)
        self.create_button(parent=self.buttonsFrame,text="Show histogram",width=buttons_width,command=lambda:histogram_window(self.image,self.image_path))
        self.create_button(parent=self.buttonsFrame,text="Apply greyscale",width=buttons_width,command=lambda: self.apply_filter(3))

        self.create_prepare_views(buttons_width)

        frame = tk.Frame(self.buttonsFrame)
        frame.pack( side = "top", padx = 5, pady = 3)

        self.create_button(parent=self.buttonsFrame,text="Min filter",width=buttons_width,command=lambda: self.apply_filter(0),pady=1)
        self.create_button(parent=self.buttonsFrame,text="Max filter",width=buttons_width,command=lambda: self.apply_filter(1),pady=1)
        self.create_button(parent=self.buttonsFrame,text="MinMax filter",width=buttons_width,command=lambda: self.apply_filter(2),pady=1)
        self.create_button(parent=self.buttonsFrame,text="Reset",width=buttons_width,command=lambda: self.load_image())
        self.create_button(parent=self.buttonsFrame,text="Save image",width=buttons_width,command=lambda: self.save_image(),pady=6)

    def create_button(self, parent, text, width, command, pady=4):
        button = tk.Button(parent , text=text, width = width, command = command)
        button.pack( side = "top", padx = 5, pady = pady)

    def create_prepare_views(self,width):
        self.gmin_string = tk.StringVar()
        self.gmax_string = tk.StringVar()
        self.create_prepare_view(width,1,lambda: self.apply_filter(4),"gmin","gmax",self.gmin_string,self.gmax_string)

        self.fmin_string = tk.StringVar()
        self.fmax_string = tk.StringVar()
        self.create_prepare_view(width,2, lambda: self.apply_filter(5),"fmin","fmax",self.fmin_string,self.fmax_string)

    def create_prepare_view(self, buttons_width, number,command,name_min,name_max,min_stringvar,max_stringvar):
        prepare_frame = tk.Frame(self.buttonsFrame)
        prepare_frame.pack( side = "top", padx = 5, pady = 4)

        self.create_button(parent=self.buttonsFrame,text="Prepare "+str(number),width=buttons_width,command=command,pady=1)

        min_frame = tk.Frame(prepare_frame)
        min_frame.pack( side = "top", padx = 5, pady = 0)

        min_label = tk.Label(min_frame, text = name_min, width = 7)
        min_label.pack(side = "left")

        min_field = tk.Entry(min_frame, textvariable=min_stringvar,width = 5)
        min_field.pack( side = "right",padx = 3)
        min_stringvar.set(30)

        max_frame = tk.Frame(prepare_frame)
        max_frame.pack( side = "top", padx = 5, pady = 0)

        max_label = tk.Label(max_frame, text = name_max, width = 7)
        max_label.pack(side = "left")

        max_field = tk.Entry(max_frame, textvariable=max_stringvar,width = 5)
        max_field.pack( side = "right",padx = 3)
        max_stringvar.set(220)

    def load_image_with_ask(self):
        self.image_path = tkFileDialog.askopenfile(mode='r',**self.file_opt)
        if self.image_path is not None:
            self.load_image()

    def load_image(self):
        file_extension = os.path.splitext(self.image_path.name)[1]
        image = Image.open(self.image_path)
        if file_extension == '.png':
            timage = Image.new("RGB", image.size, (255, 255, 255))
            timage.paste(image, mask=image.split()[3])
            image = timage
        self.change_image(image)
        self.resize_image((0,0))

    def save_image(self):
        self.file_opt['initialfile'] = "1"+ntpath.basename(self.image_path.name);
        f = tkFileDialog.asksaveasfile(mode='w', **self.file_opt )
        if f is None:
            return
        self.imagecopy.save(f)

    def apply_filter(self, id):
        image = None
        if id == 0:
            image = min_filter().apply_filter(self.imagecopy)
        if id == 1:
            image = max_filter().apply_filter(self.imagecopy)
        if id == 2:
            image = minmax_filter().apply_filter(self.imagecopy)
        if id == 3:
            image = image_processing.grayscale(self.imagecopy)
        if id == 4:
            image = image_processing.prepare1(image=self.imagecopy, gmin=int(self.gmin_string.get()), gmax=int(self.gmax_string.get()))
        if id == 5:
            image = image_processing.prepare2(image=self.imagecopy, gmin=int(self.fmin_string.get()), gmax=int(self.fmax_string.get()))
        if image != None:
            self.change_image(image)
            self.resize_image((0,0))

    def change_image(self, new_image):
        self.image = new_image
        self.imagecopy = self.image.copy()
        self.update_label_image(self.image)

    def update_label_image(self, new_image):
        img = ImageTk.PhotoImage(new_image)
        self.imageLabel.configure(image = img)
        self.imageLabel.image = img

    def resize_image(self,event):
        width, height = self.image.size
        fwidth = self.root.winfo_width()-150
        fheight = self.imageLabel.winfo_height()
        ratiow = fwidth / float(width)
        ratiof = fheight / float(height)
        ratio = min(ratiow, ratiof)
        self.image = self.imagecopy.resize((int(width*ratio), int(height*ratio)))
        self.update_label_image(self.image)
