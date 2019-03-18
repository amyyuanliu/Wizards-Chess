from tkinter import *

def startMousePressed(event, data):
    # press multi or cpu buttons
    if data.width/2-data.xSize <= event.x <= data.width/2+data.xSize:
        if data.height/2-data.ySize <= event.y <= data.height/2+data.ySize:
            data.mode = "multi"
            data.prevMode = "multi" 
        elif 2*data.height/3-20-data.ySize <= event.y <= 2*data.height/3-20+data.ySize:
            data.mode = "cpu"
            data.prevMode = "cpu"
    
def startKeyPressed(event, data):
    pass
    
def startTimerFired(data):
    pass
    
def startRedrawAll(canvas, data):
    canvas.create_image(0,0, image=data.background, anchor=NW)
    # king image
    canvas.create_image(data.width/2, data.height-20, image=data.king, anchor=S)
    #fawks
    canvas.create_image(30,10, image=data.fawks, anchor=NW)
    # logo
    canvas.create_image(data.width/2, data.height/3, image=data.logo)
    
    # multiplayer button
    canvas.create_rectangle(data.width/2-data.xSize, data.height/2-data.ySize,
                            data.width/2+data.xSize, data.height/2+data.ySize, 
                            fill="bisque2", outline="orange3",width=6)
    canvas.create_text(data.width/2, data.height/2, text="MULTIPLAYER",
                        font="Arial 26 bold")
    
    # cpu button     
    canvas.create_rectangle(data.width/2-data.xSize, 2*data.height/3-20-data.ySize,
                            data.width/2+data.xSize, 2*data.height/3-20+data.ySize, 
                            fill="bisque2", outline="orange3",width=6)
    canvas.create_text(data.width/2, 2*data.height/3-20, text="CPU",
                        font="Arial 26 bold")
    