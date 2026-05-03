#!/usr/bin/env python3
# Author: Scarlett Dixon
# Date: 2023-11-25
# Version: 0.0.1
# Usage: python __main__.py

#Generic
import time
import os
from os.path import join, dirname, exists

#File Access
import yaml

#String Manipulation
import logging
import re

#Browser Searching
from bs4 import BeautifulSoup
from autoscraper import AutoScraper

#Graphical User Interface
import tkinter as tk
from tkinter import ttk

#Personal
import passwordManager as PM

class SearcherBot():
    def __init__(self):
        print("Initialising")

    def amazonSearch():
        print("Collecting Amazon Data")

    def apexSearch():
        print("Collecting Apex Auctions Data")

    def bidspotterSearch():
        print("Collecting Bidspotter Data")

    def ebaySearch():
        print("Collecting eBay Data")

    def facebookSearch():
        print("Collecting Facebook Data")

    def neweggSearch():
        print("Collecting Facebook Data")

    def manualSearch():
        print("Collecting Manuals")

    def specificationSearch():
        print("Collecting Specifications")

    def gatherLoginData():
        print("Collecting Login Information")

    def creatingPasswordFile():
        print("Creating Password File")


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Set the window title and size.
        self.title("Marketplace Scraper")
        
        # creating a frame and assigning it to container
        container = tk.Frame(self, height=400, width=600)
        # specifying the region where the frame is packed in root
        #container.pack(side="top", fill="both", expand=True)
        
        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=3)
        # configure the grid
        #root.columnconfigure(0, weight=1)
        #root.columnconfigure(1, weight=3)

        # Add a label to the window.
        self.label = tk.Label(self, text="Click the button to start scraping Facebook Marketplace.")
        self.label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

        # Add a button to the window.
        self.button = tk.Button(self, text="Scrape Marketplace" , command=self.scrape_marketplace)
        self.button.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
        
        # Add a label to write "Developed by" to the window.
        self.label = tk.Label(self, text="Developed by: Aurora Software")
        self.label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

        
        # We will now create a dictionary of frames
        self.frames = {}
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (MainPage, SidePage, CompletionScreen):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Using a method to switch frames
        self.show_frame(MainPage)
        
        # Add Logo to the window.
        # self.logo = tk.PhotoImage(file="logo.png")
        # self.logo = self.logo.subsample(2, 2)
        # self.label = tk.Label(self, image=self.logo)
        # self.label.pack(pady=10)

    def scrape_marketplace(self):
        navigation_loc='../Configuration'
        yaml_path = join(dirname(__file__), f'{navigation_loc}/Settings.yml')
        with open(yaml_path, "r") as file:
            yaml_vars=yaml.safe_load(file)
        pass_init_path = yaml_vars['PROD']['PASSWORD_PATH']
        pass_folder = yaml_vars['PROD']['PASSWORD_FOLDER']
        pass_path = join(pass_init_path, pass_folder)
        pass_file = "password.yml"
        pass_full_path = join(pass_path, pass_file)
        print(f'{pass_full_path}')
        Bot = PM.PasswordManager()
        if (not exists(pass_full_path)):
            print(f'---Creating Password File---')
            Bot.create_password_file(pass_path, pass_file)
        else:
            try:
                print(f'---Loading Password File---')
                Bot.load_password_file(pass_full_path)
            except:
                print(f"Issues with loading file: {pass_full_path}")

    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Main Page")
        label.pack(padx=10, pady=10)

        # We use the switch_window_button in order to call the show_frame() method as a lambda function
        switch_window_button = tk.Button(
            self,
            text="Go to the Side Page",
            command=lambda: controller.show_frame(SidePage),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)


class SidePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the Side Page")
        label.pack(padx=10, pady=10)

        switch_window_button = tk.Button(
            self,
            text="Go to the Completion Screen",
            command=lambda: controller.show_frame(CompletionScreen),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)


class CompletionScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Completion Screen, we did it!")
        label.pack(padx=10, pady=10)
        switch_window_button = ttk.Button(
            self, text="Return to menu", command=lambda: controller.show_frame(MainPage)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)


if __name__ == '__main__':
    print ("hello world")
    app = MainWindow()
    app.mainloop()
