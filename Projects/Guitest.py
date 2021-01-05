#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Sat Dec 12 19:23:20 2020

#@author: scarlett

import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import matplotlib.patches as patches
    

class MainApplication(tk.Frame):
    #Standard GUI creation
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure_gui()
        self.create_widgets()
    
    def configure_gui(self):
       self.parent.title("Shape Net Creation")
       self.parent.geometry("650x400")
       self.parent.resizable(False, False)
       
    def create_widgets(self):
        #self.create_menu() #For if I wish to add a menu in future
        self.create_main()
        
    def create_main(self):
        #All very straightforward and understandable, new items are added going down
        gridrow = 0
        gridcol = 0
        
        Meas = tk.Label(self.parent, text="Please decide on the measurent you'd like to use (Default Inches):")
        Meas.grid(row=gridrow,column=gridcol)
        gridrow += 1
        
        self.meas = tk.IntVar()
        Cent = tk.Radiobutton(self.parent, text="Centimetres", variable=self.meas, value=1)
        Cent.grid(row=gridrow,column=0)
        Inch = tk.Radiobutton(self.parent, text="Inches", variable=self.meas, value=2)
        Inch.grid(row=gridrow,column=1)
        gridrow += 1
        
        Dime = tk.Label(self.parent, text="Please enter the dimensions of your cube/oid:")
        Dime.grid(row=gridrow,column=0); gridrow += 1
        
        Leng = tk.Label(self.parent, text="Length (x):")
        Leng.grid(row=gridrow,column=0)
        self.len = tk.DoubleVar()
        LengEnt = tk.Entry(self.parent, textvariable =self.len)
        LengEnt.grid(row=gridrow,column=1)
        gridrow += 1
        
        Hei = tk.Label(self.parent, text="Height (y):")
        Hei.grid(row=gridrow,column=0)
        self.hei = tk.DoubleVar()
        HeiEnt = tk.Entry(self.parent, textvariable =self.hei)
        HeiEnt.grid(row=gridrow,column=1)
        gridrow += 1
        
        Wid = tk.Label(self.parent, text="Width (z):")
        Wid.grid(row=gridrow,column=0)
        self.wid = tk.DoubleVar()
        WidEnt = tk.Entry(self.parent, textvariable =self.wid)
        WidEnt.grid(row=gridrow,column=1)
        gridrow += 1
        
        Cir = tk.Label(self.parent, text="Circle Radius:")
        Cir.grid(row=gridrow,column=0)
        self.cir = tk.DoubleVar()
        CirEnt = tk.Entry(self.parent, textvariable =self.cir)
        CirEnt.grid(row=gridrow,column=1)
        gridrow += 1
        
        DpiLab = tk.Label(self.parent, text="Please enter image dpi (Default = 400)")
        DpiLab.grid(row=gridrow,column=0); gridrow += 1
        
        Dpi = tk.Label(self.parent, text="DPI:")
        Dpi.grid(row=gridrow,column=0)
        self.dpi = tk.DoubleVar()
        DpiEnt = tk.Entry(self.parent, textvariable =self.dpi)
        DpiEnt.grid(row=gridrow,column=1)
        gridrow += 1
        
        
        Exten = tk.Label(self.parent, text="Please choose an extension to save the file as (Default PNG):")
        Exten.grid(row=gridrow,column=0)
        gridrow += 1
        
        self.exten = tk.IntVar()
        Png = tk.Radiobutton(self.parent, text="PNG", variable=self.exten, value=1)
        Png.grid(row=gridrow,column=0)
        Jpg = tk.Radiobutton(self.parent, text="JPG", variable=self.exten, value=2)
        Jpg.grid(row=gridrow,column=1)
        gridrow += 1
        Pdf = tk.Radiobutton(self.parent, text="PDF", variable=self.exten, value=3)
        Pdf.grid(row=gridrow,column=0)
        gridrow += 1
        
        Tab = tk.Label(self.parent, text="Do you wish to have tabs added (Default No)?:")
        Tab.grid(row=gridrow,column=0)
        gridrow += 1
        
        self.tab = tk.IntVar()
        TabYes = tk.Radiobutton(self.parent, text="Yes", variable=self.tab, value=1)
        TabYes.grid(row=gridrow,column=0)
        TabNo = tk.Radiobutton(self.parent, text="No", variable=self.tab, value=2)
        TabNo.grid(row=gridrow,column=1)
        gridrow += 1
        
        FinalButt = tk.Button(self.parent,text="Begin",command=self.beginclick)
        FinalButt.grid(row=gridrow,column=0)
    
    def beginclick(self):
        ## Initialisation of the mapping software
        Backend(self.meas.get(), self.len.get(), self.hei.get(),self.wid.get(), self.cir.get(), self.exten.get(), self.dpi.get(), self.tab.get())
        #self.parent.quit() #Can crash if the correct closing is not used
        self.parent.destroy()
        #else:
            #Err.grid(row=8,column=0)
            
class Backend():
    def __init__(self, meas, l, h, w, cirR, exten, dpi, tab):
        #Might eventually make all variables related to their specific classes so as to not have to pass them through
        self.dpi = dpi
        self.tab = tab
        if (meas == 1):
            #print("Centimetres")
            l, h, w, cirR = self.cm_to_inch(l, h,w, cirR)
            self.data(l, h,w, cirR, exten)
        else:
            #print("Inches")
            self.data(l, h,w, cirR, exten)
            
    def cm_to_inch(self, inpl,inph,inpw,inpr):
        #Self explanatory, converts centimetres to 
        outl = (inpl/2.54)
        outh = (inph/2.54)
        outw = (inpw /2.54)
        outr = (inpr /2.54)
        return outl,outh,outw, outr
    
    def data(self, l, h, w, cirR, exten):
        #Area to craft the outline of the figure and the map initial         
        self.dimensions = [l,h,w]
        self.largest = max(self.dimensions)
        self.smallest =min(self.dimensions)
        #The order for the placement of the initial rectangles are:
        #Middle 1; Middle 2; Middle 3; Middle 4; Right 2; Left,2
        self.locations = [(w, 0), (w,w), (w, w + h), (w, w + h + w), (l + w, w), (0, w)]
        self.sizes = [[l,w], [l,h], [l,w], [l,h],[w,h],[w,h]]
        self.origin = (2*self.smallest,2*self.smallest)
        self.figsiz = [(l+w+w+self.origin[0]+self.origin[0]),(h+w+h+w+self.origin[1]+self.origin[1])]
        self.angle = self.smallest / 10
        self.thickness = self.smallest / 2
        self.automate(l, h, w, cirR, exten)
        
    def tabdata(self,l,h,w):
        #Area for the addition of tab data
        angle = self.angle
        thickness = self.thickness
        middlebottom = [(w,0),(l+w,0),(l+w-(angle),-thickness), (w+(angle),-(thickness))]
        leftmiddle = [(-thickness, w+h-(angle)),(0,w+h), (0,w), (-(thickness),w+(angle)) ]
        lefttop = [(0+(angle),w+h+(thickness)),(w-(angle),w+h+(thickness)),(w,w+h), (0,w+h)]
        leftbottom = [(0,w), (w,w), (w-angle, w-thickness),(0+angle,w-thickness)]
        rightmiddle = [(w+l+w,w+h),(w+l+w+ thickness,w+h-angle),(w+l+w+thickness,w+angle),(w+l+w,w)]
        righttop =[(w+l+angle,w+h+thickness),(w+l+w-angle,w+h+thickness),(w+l+w,w+h), (w+l,w+h)]
        rightbottom = [(w+l,w),(w+l+w,w),(w+l+w-angle,w-thickness),(w+l+angle,w-thickness)]
        Tabs = [middlebottom, leftmiddle, lefttop, leftbottom, rightmiddle, righttop, rightbottom]
        return Tabs
    def automate(self, l, h, w, cirR, exten):
        if (self.dpi == 0.0 or self.dpi == 0):
            self.dpi= 400
        fig = plt.figure(figsize=self.figsiz,dpi=self.dpi)
        ax = fig.add_axes([0,0,1,1])
        ax.axis('off')
        for lo,s in zip(self.locations,self.sizes):
            ax.add_patch(plt.Rectangle(np.array(self.origin)+np.array(lo),s[0], s[1], ec='black',fc='None', transform=fig.dpi_scale_trans))
        ax.add_patch(plt.Circle(((self.origin[0]+ w+(l/2)),(self.origin[1]+w+h+w+(h/2))), radius=cirR, ec='black',fc='None', transform=fig.dpi_scale_trans))
        if (self.tab == 1):
            Tabs = self.tabdata(l,h,w)
            for tab in Tabs:
                ax.add_patch(patches.Polygon(xy=(np.array(self.origin)+np.array(tab)), fill=False, transform=fig.dpi_scale_trans))
            
        if (exten == 2):
            fig.savefig('Map.jpg', format='jpg')
        elif (exten ==3):
            fig.savefig('Map.pdf', format='pdf')
        else:
            fig.savefig('Map.png', format='png')
        
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)#.pack(side="top", fill="both", expand=True)
    root.mainloop()    
    
"""
#test = self.len.get()
#LengLabel = tk.Label(self.parent, text=test)
#LengLabel.grid(row=8,column=0)
#print(self.len.get())
#Err.grid_forget()
LengLabel = tk.Label(self.parent, text=self.len.get())
            LengLabel.grid(row=8,column=0)
fig = plt.figure()
#fig.set_size_inches(self.figsiz[0],self.figsiz[1])
fig.set_size_inches(10,13)
#ax = plt.axes(xlim=(0, 200), ylim=(0, 200))
for x in range (6):
    plt.gca().add_patch(plt.Rectangle(self.locations[x],self.sizes[x][0], self.sizes[x][1], ec='black',fc='None'))
plt.gca().add_patch(plt.Circle(((w+(l/2)),(w+h+w+(h/2))), radius=cirR, ec='black',fc='None'))
print(cirR)
plt.axis('scaled')
#plt.axis('off')
plt.tight_layout()
plt.show()
fig.savefig('Map.png')
#fig = plt.figure(figsize=(12,12),dpi=self.dpi)
        #print(self.figsiz)
"""