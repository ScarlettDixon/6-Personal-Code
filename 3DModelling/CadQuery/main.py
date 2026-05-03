#!/usr/bin/env python
# coding: utf-8

import sys
import fnmatch
import tkinter as tk

from os import listdir
from tkinter import ttk
from subprocess import run

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("320x100")
        self.title('Tkinter OptionMenu Widget')
        self.file_list= []
        self.file_location= 'BuildFiles'

        # initialize data
        self.cadquery_files()

        # set up variable
        self.option_var = tk.StringVar(self)

        # create widget
        self.create_wigets()

    def create_wigets(self):
        # padding for widgets using the grid layout
        paddings = {'padx': 5, 'pady': 5}

        # label
        label = ttk.Label(self,  text='Select Which File to Load:')
        label.grid(column=0, row=0, sticky=tk.W, **paddings)

        # option menu
        option_menu = ttk.OptionMenu(
            self,
            self.option_var,
            self.file_list[0],
            *self.file_list,
            command=self.option_changed)

        option_menu.grid(column=1, row=0, sticky=tk.W, **paddings)

        btn = ttk.Button(self, text='Load', command=self.return_pressed)
        btn.grid(column=0, row=2, sticky=tk.W, **paddings)

        # output label
        self.output_label = ttk.Label(self, foreground='red')
        self.output_label.grid(column=0, row=1, sticky=tk.W, **paddings)

    def option_changed(self, *args):
        self.output_label['text'] = f'You selected: {self.option_var.get()}'

    def return_pressed(self, *args):
        run([sys.executable, f'{self.file_location}/{self.option_var.get()}'])
    
    def cadquery_files(self, *args):
        listOfFiles = listdir(self.file_location)
        pattern = "*.py"
        for entry in listOfFiles:
            if fnmatch.fnmatch(entry, pattern) and entry != "main.py":
                    self.file_list.append(entry)
        #print (self.file_list)

if __name__ == '__main__':
    app = App()
    app.mainloop()
    #OptionMenu(container, variable, default=None, *values, **kwargs)



#Bibliography:
#https://www.pythontutorial.net/tkinter/tkinter-optionmenu/