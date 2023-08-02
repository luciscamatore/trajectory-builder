from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import numpy as np
import subprocess as sp
import time

selector = Tk();
selector.title('Dimension Selector')
selector.geometry("600x400")

#width= window.winfo_screenwidth()
#height= window.winfo_screenheight()
#window.geometry("%dx%d" % (width,height))


coordonate = []
lungime = 0
latime = 0
liniiX = []
liniiY = []
actionPressed = False
actionCode = []
numberOfActions = 200

def openWindow():
    
    lungime = int(inputLungime.get())
    latime = int(inputLatime.get())

    constructor = Tk()
    constructor.geometry("900x600")
    constructor.title('Trajectory Builder')

    pointList = []
    lineList = []
    def drawGrid():
        for i in range(0, lungime*10, 10):
            canvas.create_line(1 ,i, lungime*10, i, fill="#e6e6e6", width=2)
            liniiX.append(i)
        for i in range(0, latime*10, 10):
            canvas.create_line(i ,1, i, latime*10, fill="#e6e6e6", width=2)
            liniiY.append(i)
    
    def drawPoints(event):
        global numberOfActions
        x1 = canvas.canvasx(event.x)
        y1 = canvas.canvasy(event.y)
        coordX = min(liniiX, key=lambda x:abs(x-x1))
        coordY = min(liniiY, key=lambda y:abs(y-y1))

        color = 'black'
        width = 4
        opt = 0
        if actionPressed:
            color = 'blue'
            width = 6
            variable = StringVar(constructor)
            variable.set("Select")
            opt = OptionMenu(constructor, variable, "1", "2", "3")
            opt.place(x=800, y=numberOfActions)
        else:
            color = 'black'
            width = 4
            actionCode = 0

        oval = canvas.create_oval(coordX,coordY,coordX,coordY,outline=color,width=width)
        label = canvas.create_text(coordX+22, coordY-13, text="["+str(int(coordX/10)) + ", " + str(int(coordY/10))+"]")
        
        numberOfActions += 50
        coordonate.append([coordX,coordY])
        pointList.append([coordX, coordY, oval, label, opt])
        

    def deletePoints(event):
        x1 = canvas.canvasx(event.x)
        y1 = canvas.canvasy(event.y)
        coordX = min(liniiX, key=lambda x:abs(x-x1))
        coordY = min(liniiY, key=lambda y:abs(y-y1))

        for point in pointList:
            if (point[0] == coordX) and (point[1] == coordY):
                canvas.delete(point[2])
                canvas.delete(point[3])
                canvas.delete(point[4])
                coordonate.remove([coordX, coordY])

        for line in lineList:
            if((line[0] == coordX) and (line[1] == coordY)) or ((line[2] == coordX) and (line[3] == coordY)):
                canvas.delete(line[4])


    def connectLines():
        for i in range(len(coordonate)-1):
            line = canvas.create_line(coordonate[i][0],coordonate[i][1], coordonate[i+1][0],coordonate[i+1][1], fill="red", width=2,arrow=tk.LAST)
            lineList.append([coordonate[i][0],coordonate[i][1], coordonate[i+1][0],coordonate[i+1][1], line])

    def clearCanvas():
        canvas.delete('all')
        coordonate.clear()
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
        sp.run(["python", "trajectory.py"])

    
    def actionIsPressed():
        global actionPressed

        if actionPressed:
            actionPressed = False
            butonAction.config(background="SystemButtonFace")
        else:
            actionPressed=True
            butonAction.config(background="green")
    

    selector.destroy()
    frame = Frame(constructor, width=800, height=900)
    frame.pack(expand=True, fill= BOTH)
    
    canvas = Canvas(frame,width=lungime*20,height=latime*20, bg="white", scrollregion=(0,0,lungime*10,latime*10))

    vbar=Scrollbar(frame,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)

    hbar=Scrollbar(frame,orient=HORIZONTAL)
    hbar.pack(side=BOTTOM,fill=X)
    hbar.config(command=canvas.xview)

    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set) 

    canvas.pack(padx=(20,100), pady=(20))

    canvas.bind('<Button-1>', drawPoints)
    canvas.bind('<Button-2>', move_from)
    canvas.bind('<B2-Motion>', move_to)
    canvas.bind('<Button-3>', deletePoints)
    
    canvas2 = Canvas(frame, width=900, height=600, bg='white')
    canvas2.pack(padx=5,pady=5)

    canvas2.create_line(5,5,800,5,fill='black',width=5)

    drawGrid()
    
    # BUTTONS
    butonConnect = Button(constructor,text="Connect",width=7,height=1,command=connectLines,bd='5')
    butonConnect.place(x=800,y=5)

    butonClear = Button(constructor,text="Clear",width=7,height=1,command=clearCanvas,bd='5')
    butonClear.place(x=800,y=50)

    butonAction = Button(constructor,text = "Actions", width=7, height=1,bd='5',background='SystemButtonFace', command=actionIsPressed)
    butonAction.place(x=800,y=100)

    butonWrite = Button(constructor, text="Generate", width=7, height=1,bd='5', command=writeToFile)
    butonWrite.place(x=800,y=150)
    # LINES
    #canvas.create_line(10,-10, 800,-10, fill='black', width=2)
    sp = ttk.Separator(constructor, orient='horizontal')
    sp.pack(padx=100, pady=10, fill='x')
    constructor.mainloop()

def openConditions():
    try:
        float(lungime)
        float(latime)
        openWindow()
    except ValueError:
        print("niu")
        messagebox.showerror("Error!","Values must be numeric")


canvas = tk.Canvas(selector, width=600,height=400)
canvas.pack()

inputLatime = tk.Entry(selector)
inputLungime = tk.Entry(selector)

labelLungime = tk.Label(selector, text="Lungime",font=("UbuntuMono",9))
labelLatime = tk.Label(selector, text="Latime",font=("UbuntuMono",9))
labelMetri = tk.Label(selector, text="METRI",font=("UbuntuMono",9))

canvas.create_window(80, 100, window=labelLungime)
canvas.create_line(80,100,230,100,width=2,fill="#FF6161",arrow=tk.LAST)

canvas.create_window(80, 200, window=labelLatime)
canvas.create_line(80,200,230,200,width=2,fill="#FF6161",arrow=tk.LAST)

canvas.create_window(300, 100, window=inputLungime)
canvas.create_window(300, 200, window=inputLatime)

canvas.create_line(300,100,400,100,width=2,fill="#FF6161")
canvas.create_line(300,200,400,200,width=2,fill="#FF6161")

canvas.create_line(400,100,400,145,width=2,fill="#FF6161")
canvas.create_line(400,200,400,155,width=2,fill="#FF6161")

canvas.create_line(400,145,450,145,width=2,fill="#FF6161",arrow=tk.LAST)
canvas.create_line(400,155,450,155,width=2,fill="#FF6161",arrow=tk.LAST)

canvas.create_window(470, 150, window=labelMetri)

canvas.create_line(470,150,470,265,width=2,fill="#FF6161")
canvas.create_line(470,265,340,265,width=2,fill="#FF6161",arrow=tk.LAST)

butonOpen = Button(selector, text="Continue", width=7, height=1,bd='5',command=openConditions)
butonOpen.place(x=270,y=250)

selector.bind("<Return>", openConditions)

selector.mainloop()


'''
    def move_to(event):
        canvas.scan_dragto(event.x, event.y, gain=1)
        global afterPan
        afterPan = [event.x, event.y]
        print("afterPan", afterPan)

    def move_from(event):
        canvas.scan_mark(event.x, event.y)
        global startPan
        startPan = [event.x, event.y]
        print("START", startPan)

    def scroll(event):
        if(event.delta > 0):
            canvas.scale("all", event.x, event.y, 1.1, 1.1)
        if(event.delta < 0):
            canvas.scale("all", event.x, event.y, 0.9, 0.9)
'''