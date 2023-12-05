from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import _flatten, _cnfmerge
import numpy as np
import subprocess
import time

#width= window.winfo_screenwidth()
#height= window.winfo_screenheight()
#window.geometry("%dx%d" % (width,height))

constructor = tk.Tk()
constructor.geometry("900x600")
constructor.title('Trajectory Builder')

coordonate = []
lungime = 0
latime = 0
liniiX = []
liniiY = []
actionPressed = False
zonePressed = False
robotPressed = False
actionCode = []
numberOfActions = 200
newX = -1
newY = -1
zoneCoords = []
zoneLineCoords=[]
itemsToKeep = []
pointList = []
points = []
lineList = []
robotzel = 0

def drawGrid():
    dimensiuneX = 400
    dimensiuneY = 400
    for i in range(-dimensiuneX, dimensiuneX, 10):
        canvas.create_line(-dimensiuneX ,i, dimensiuneX, i, fill="#e6e6e6", width=2)
        liniiX.append(i)
    for i in range(-dimensiuneY, dimensiuneY, 10):
        canvas.create_line(i ,-dimensiuneY, i, dimensiuneY, fill="#e6e6e6", width=2)
        liniiY.append(i)

    canvas.create_oval(-5,-5,5,5, fill="black")

    canvas.create_text(100,10, text="X", font='Helvetica 10 bold')
    canvas.create_line(-400,0,400,0,fill="black", width=1)
    canvas.create_line(5,0,100,0,fill="red",  width=4,arrow=tk.LAST)

    canvas.create_line(0,-300,0,300,fill="black", width=1)
    canvas.create_text(10,-100, text="Y", font='Helvetica 10 bold')
    canvas.create_line(0,-3,0,-100,fill="green",  width=4,arrow=tk.LAST)

def drawRobot():
    global robotPressed
    global robotzel
    if robotPressed:
        robotPressed = False
        canvas.delete("robot")
        canvas.delete("sageata")
        butonRobot.config(background="SystemButtonFace")
    else:
        #                      x1  y1  x2  y2  x3  y3  x4  y4  x5  y5  x6  y6  x7  y7  x8  y8
        robotzel = canvas.create_polygon(-40,-30, 40,-30,-40, 30, 40, 30,-40,-30,-40, 30, 40,-30, 40, 30, fill="orange", tag="robot")
        canvas.create_line(-20,0,20,0,fill="black",width=3, arrow=tk.LAST, tag="sageata")
        robotPressed = True
        butonRobot.config(background="green")
    

def drawPoints(event):
    x1 = canvas.canvasx(event.x)
    y1 = canvas.canvasy(event.y)
    coordX = min(liniiX, key=lambda x:abs(x-x1))
    coordY = min(liniiY, key=lambda y:abs(y-y1))

    color = 'black'
    width = 4
   
    oval = canvas.create_oval(coordX,coordY,coordX,coordY,outline=color,width=width)
    label = canvas.create_text(coordX+22, coordY-13, text="[x:"+str(int(coordX)) + ", y:" + str(int(-coordY))+"]")
    
    coordonate.append([coordX,-coordY])
    pointList.append([coordX, -coordY, oval, label])
    points.append((coordX,coordY))

def deletePoints(event):
    global pointList
    global coordonate
    x1 = canvas.canvasx(event.x)
    y1 = canvas.canvasy(event.y)
    coordX = min(liniiX, key=lambda x:abs(x-x1))
    coordY = min(liniiY, key=lambda y:abs(y-y1))

    found = False
    pointsToKeep = []
    coordsToKeep = []
    for point in pointList:
        if not found:
            pointsToKeep.append(point)
            coordsToKeep.append([point[0], point[1]])
        if found:            
            canvas.delete(point[2])
            canvas.delete(point[3])
        if (point[0] == coordX) and (point[1] == -coordY):
            found = True
            canvas.delete(point[2])
            canvas.delete(point[3])

    del pointsToKeep[-1]
    del coordsToKeep[-1]
    pointList = pointsToKeep
    coordonate = coordsToKeep

    found = False
    for line in lineList:
        if found:
            canvas.delete(line[4])
        if((line[0] == coordX) and (line[1] == coordY)) or ((line[2] == coordX) and (line[3] == coordY)):
            found = True
            canvas.delete(line[4])
     

def connectLines():
    line = canvas.create_line(0,0,coordonate[0][0],-coordonate[0][1],fill="#000099", width=2,arrow=tk.LAST)
    lineList.append([0,0,coordonate[0][0],-coordonate[0][1], line])
    for i in range(len(coordonate)-1):
        line = canvas.create_line(coordonate[i][0],-coordonate[i][1], coordonate[i+1][0],-coordonate[i+1][1], fill="#000099", width=2,arrow=tk.LAST)
        lineList.append([coordonate[i][0],-coordonate[i][1], coordonate[i+1][0],-coordonate[i+1][1], line])
        
def interpolate_bezier(points, num_points):
    result = []
    for i in range(num_points):
        t = i / (num_points - 1)
        x = sum((1 - t) ** (len(points) - 1 - i) * t ** i * p[0] for i, p in enumerate(points))
        y = sum((1 - t) ** (len(points) - 1 - i) * t ** i * p[1] for i, p in enumerate(points))
        result.append((x, y))
    return result

def smoothLines():
    for line in lineList:
        canvas.delete(line[4])
    points.insert(0,[0,0])
    flattened = [a for x in points for a in x]
    canvas.create_line(*flattened, width=2, fill="#3333FF", arrow=tk.LAST, smooth=1, splinesteps=100)

    spline_points = interpolate_bezier(points, 100)

    f = open("spline_points.txt", "w")
    try:
        for i in spline_points:
                f.write(str(i).replace("[","").replace("]","").replace("(","").replace(")","") + "\n")
    finally:
        f.close()
    
def drawZoneLines(coordX, coordY):
    global newX 
    global newY
    lastX = coordX
    lastY = coordY
    zoneCoords.append([coordX, coordY])
    if (newX == -1) and (newY == -1):
        newX = lastX
        newY = lastY
    if ((lastX != newX) or (lastY != newY)):
        zoneLineCoords.append(canvas.create_line(newX,newY,lastX, lastY, fill="red", width=2))
        newX = lastX
        newY = lastY
    itemsToKeep = zoneCoords + zoneLineCoords

def drawZonePoints(event):
    x1 = canvas.canvasx(event.x)
    y1 = canvas.canvasy(event.y)
    coordX = min(liniiX, key=lambda x:abs(x-x1))
    coordY = min(liniiY, key=lambda y:abs(y-y1))

    canvas.create_oval(coordX,coordY,coordX,coordY,outline="red",width=6)

    drawZoneLines(coordX, coordY)

# def connectZones():
#     global zonePressed
#     if zonePressed:
#         zonePressed = False
#         butonZones.config(background="SystemButtonFace")
#     else:
#        zonePressed=True
#        butonZones.config(background="green")

#     if zonePressed:
#         canvas.unbind('<Button-1>')
#         canvas.bind('<Button-1>', drawZonePoints)
#     else:
#         canvas.unbind('<Button-1>')
#         canvas.bind('<Button-1>', drawPoints)

def clearCanvas():
    # itemsToKeep ca si parametru
    # for item_id in canvas.find_all():
    #     if item_id not in itemsToKeep:
    #             canvas.delete(item_id)
        
    canvas.delete('all')
    coordonate.clear()
    points.clear()
    pointList.clear()
    drawGrid()

def move_to(event):
    canvas.scan_dragto(event.x, event.y, gain=1)

def move_from(event):
    canvas.scan_mark(event.x, event.y)

def writeToFile():
    f = open("input.txt", "w")
    try:
        for i in range(0, len(coordonate), 1):
            for j in range(0,2,1):
                f.write(str(coordonate[i][j]/10) + ",")
    finally:
        f.close()
        
    subprocess.run(["python", "trajectory.py"])

    
def actionIsPressed():
    global actionPressed
    if actionPressed:
        actionPressed = False
        butonRobot.config(background="SystemButtonFace")
    else:
        actionPressed=True
        butonRobot.config(background="green")

def zoneIsPressed():
    global zonePressed
    if zonePressed:
        zonePressed = False
        butonRobot.config(background="SystemButtonFace")
    else:
        zonePressed=True
        butonRobot.config(background="green")     
def animateRobot():
    for i in coordonate:
        canvas.move(robotzel, i[0],i[1])

canvas = Canvas(constructor,width=800,height=900, bg="white")
canvas.pack(expand=True, fill= BOTH)
# vbar=Scrollbar(frame,orient=VERTICAL)
# vbar.pack(side=RIGHT,fill=Y)
# vbar.config(command=canvas.yview)

# hbar=Scrollbar(frame,orient=HORIZONTAL)
# hbar.pack(side=BOTTOM,fill=X)
# hbar.config(command=canvas.xview)

# canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set) 

canvas.pack(padx=(1,125), pady=(1))
canvas.old_coords = None

    
canvas.bind('<Button-1>', drawPoints)
canvas.bind('<Button-2>', move_from)
canvas.bind('<B2-Motion>', move_to)
canvas.bind('<Button-3>', deletePoints)    

drawGrid()


canvas.configure(scrollregion=(-400,-300, 400, 300))
canvas.xview_moveto(.5)
canvas.yview_moveto(.5)

# BUTTONS
butonConnect = Button(constructor,text="Connect",width=7,height=1,command=connectLines,bd='5')
butonConnect.place(x=800,y=5)

# butonZones = Button(constructor,text="Zone",width=7,height=1,command=connectZones,bd='5')
# butonZones.place(x=800,y=50)

butonClear = Button(constructor,text="Clear",width=7,height=1,command=clearCanvas,bd='5')
butonClear.place(x=800,y=50)

butonSpline = Button(constructor, text="Smooth", width=7, height=1, bd='5', command=smoothLines)
butonSpline.place(x=800,y=100)

butonWrite = Button(constructor, text="Generate", width=7, height=1,bd='5', command=writeToFile)
butonWrite.place(x=800,y=150)

butonRobot = Button(constructor,text = "Robot", width=7, height=1,bd='5',background='SystemButtonFace', command=drawRobot)
butonRobot.place(x=800,y=200)

ButonAnimate = Button(constructor, text="Animate", width=7, height=1, bd='5', command=animateRobot)
ButonAnimate.place(x=800, y=250)




constructor.mainloop()
