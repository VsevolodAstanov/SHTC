from tkinter import *
from shtc.shtc import TagCounter


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master