#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import math
from pathlib import Path
from typing import TYPE_CHECKING
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, Polygon

include_dir = Path(__file__).parent / "Include"
sys.path.append(str(include_dir))

def include_files():
    # Get proper type hinting without impacting runtime
    if TYPE_CHECKING:
        from .Include import PythonScript
    else:
        import PythonScript

    #print(os.environ)



if __name__ == '__main__':
    include_files()
    sizes=[
        ["A3", 297, 420],
        ["A4", 210, 297],
        ["A5", 148, 210],
        ["A6", 105, 148],
        ["A7", 74, 105],
        ]
    print(sizes[2][1])
    #fig, ax = plt.subplots()
    
    #ax.add_patch(
    Book_Width = sizes[2][1]
    Book_Height =  sizes[2][2]
    Start_Pos = [100,100]
    rec_pts = np.array([[Start_Pos[0], Start_Pos[1]],[Start_Pos[0]+Book_Width,Start_Pos[1]],[Start_Pos[0]+Book_Width,Start_Pos[1]+Book_Height],[Start_Pos[0], Start_Pos[1]+Book_Height]])
    rectangle = plt.Polygon(rec_pts, edgecolor='blue', facecolor='lightblue')
    #rectangle = plt.Rectangle(xy=(Start_Pos[0], Start_Pos[1]), width=Book_Width, height=Book_Height)#, edgecolor='blue', facecolor='lightblue')
    #Triangle 0.0
    T00A_Angle = 90
    T00BC = math.sqrt((Book_Width*Book_Width)+(Book_Height*Book_Height))
    T00AB = Book_Width
    TOOAC = Book_Height
    T00B_Angle=math.degrees(math.atan(TOOAC/T00AB))
    print(f"TOOB_Angle: {T00B_Angle}")
    T00C_Angle=180 - (T00A_Angle+T00B_Angle)
    print(f"T00C_Angle: {T00C_Angle}")

    #Triangle 1.0
    #∠A=90◦
    T10A_Angle = 90
    #a^2 = b^2 + c^2
    #BC=√W^2+H^2
    T10BC = T00BC
    print(T10BC)
    # ∠C=θ
    # You decide what θ is, will test what changes it makes, must be smaller than 45 degrees and likely smaller that 22.5
    T10C_Angle = 20
    T10B_Angle = 180 - (T10A_Angle + T10C_Angle)
    # AC=BC cos(θ)
    T10AC = T10BC * math.cos(T10C_Angle)
    print(f"T10AC: {T10AC}")
    # AB=BCsin(θ )
    T10AB = T10BC * math.sin(T10C_Angle)
    print(f"T10AB: {T10AB}")

    #Triangle 1.1
    #Right Angle
    T11A_Angle = 90
    #
    T11BC = T10AB
    T11B_Angle = 180 - (T00B_Angle + T10B_Angle)
    T11C_Angle = 180 - (T11A_Angle + T11B_Angle)
    T11AC = T11BC * math.sin(T11B_Angle)
    print(f"T11AC: {T11AC}")
    T11AB = T11BC * math.sin(T11C_Angle)
    print(T11AB)
    #triangle10_pts = np.array([[Start_Pos[0], Start_Pos[1]],[Start_Pos[0],Start_Pos[1]+T10AC],[Start_Pos[0]+T10AB, Start_Pos[1]]])
    triangle10_pts = np.array([[Start_Pos[0]+Book_Width,Start_Pos[1]],[Start_Pos[0],Start_Pos[1]+Book_Height],[Start_Pos[0]-T11AB, Start_Pos[1]+Book_Height-T11AC]])
    triangle10 = plt.Polygon(triangle10_pts, edgecolor='red', facecolor='lightblue')


    #Triangle 2
    # DC=W
    T2DC=Book_Width
    # BE=H
    T2BE=Book_Height
    # AD=√((W^2 * sin(θ)) + (H^2 * cos(θ)) - (H * W* sin(2*θ)))
    # AB=BC * sin(θ)
    #T2AB = T10BC * math.sin(0)
    # AD=√((W^2 * sin^2(θ))+(H^2 * cos^2(θ) − H * W * sin(2*θ))
    #∠E=∠BEA=φ
    #AE=√H^2 * cos^2(θ )−W^2 * sin^2(θ)
    #φ =arcsin((√H^2 * cos^2(θ )−W2sin2(θ ))/H)

    #pts = np.array([[2,2], [6,5], [3,np.sqrt(5**2 - 2**2)]])

    
    plt.gca().add_patch(rectangle)
    plt.gca().add_patch(triangle10)
    plt.axis('scaled')
    #ax.set_aspect('equal')
    #plt.grid(True)
    plt.title('Drawing Shapes in Matplotlib')
    plt.show()

    