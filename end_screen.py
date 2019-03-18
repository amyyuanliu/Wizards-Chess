from tkinter import *
from chess_classes import *

def endMousePressed(event, data):
    pass
    
def endTimerFired(data):
    pass
    
def endRedrawAll(canvas, data):
    # background
    canvas.create_image(0,0, image=data.background, anchor=NW)
    # logo
    canvas.create_image(data.width/2, data.topScreen + 10, image=data.logo)
    # middle decor
    playHeight = 8 * data.cellSize + 2 * data.margin + data.topScreen
    canvas.create_image(data.width/2, playHeight/2+20, image=data.broomstick)
    canvas.create_image(data.width/2, playHeight/2+30, image=data.platform) 
    # time
    seconds = data.timer/12 # personally matched up w time
    min = seconds//60
    sec = seconds%60
    canvas.create_text(data.width- 40,10,text="Elapsed Time: %d min, %d sec" %(min,sec), 
            font="Arial 24 bold", fill="white", anchor=NE)
    
    
    # white
    canvas.create_rectangle(data.margin, data.margin+data.topScreen, 
            data.width/2-data.margin, data.margin+data.topScreen+8*data.cellSize,
            fill="", outline="white", width=4)
    canvas.create_text(data.width/4, data.margin+data.topScreen+8*data.cellSize+10,
            text="White Pieces Taken", font="Arial 26 bold", fill="white", anchor=N)
    x = data.margin + data.cellSize
    y = data.topScreen + data.margin + data.cellSize
    for piece in data.takenWhite:
        canvas.create_image(x,y, image=piece.image)
        x += data.cellSize
        if x > data.width/2 - (data.margin + data.cellSize):
            y += data.cellSize
            x = data.margin + data.cellSize
            
    # black
    canvas.create_rectangle(data.width/2+data.margin, data.margin+data.topScreen, 
            data.width-data.margin, data.margin+data.topScreen+8*data.cellSize,
            fill="", outline="white", width=4)
    canvas.create_text(3*data.width/4, data.margin+data.topScreen+8*data.cellSize+10,
            text="Black Pieces Taken", font="Arial 26 bold", fill="white", anchor=N)
            
    canvas.create_text(data.width/2, data.height-20, anchor=S, fill="bisque2",
                text="[ PRESS SPACE TO PLAY AGAIN ]", font="Arial 30 bold")
    i = data.width/2 + data.margin + data.cellSize
    j = data.topScreen + data.margin + data.cellSize
    for piece in data.takenBlack:
        canvas.create_image(i,j, image=piece.image)
        i += data.cellSize
        if i > data.width - (data.margin + data.cellSize):
            j += data.cellSize
            i = data.width/2 + data.margin + data.cellSize