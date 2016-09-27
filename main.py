#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter as tk
from view import ApplicationView
from PIL import ImageTk, Image

class MyApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.root = self
        self.view = ApplicationView()
        self.view.initialize(self)

if __name__ == "__main__":
    app = MyApplication()
    app.title('MISOI KR1')
    app.geometry('1000x600');
    app.minsize(600, 400)
    app.mainloop()
