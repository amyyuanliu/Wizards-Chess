from tkinter import *
from chess_classes import *

def rulesKeyPressed(event, data):
    if event.keysym == "Tab":
        data.mode = "multi"
    
def rulesMousePressed(event, data):
    pass
    
def rulesTimerFired(data):
    pass
    
def rulesRedrawAll(canvas, data):
    # background
    canvas.create_image(0,0, image=data.background, anchor=NW)
    # logo
    canvas.create_image(data.width/2, data.topScreen + 10, image=data.logo)
    
    ## RULES
    rules = [
    ("This game follows the rules of normal chess, but with special features:"),
    ("To move a piece, press [SPACE] to enter a voice command. ENUNCIATE CLEARLY."),
    ("IMPORTANT - after pressing [SPACE], wait for the cursor to start loading"),
    ("before talking. For Macs, this will look like         . ENUNCIATE CLEARLY!"),
    ("Otherwise, you can also type a command in the text box at the bottom."),
    ("IMPORTANT - Commands must follow the following format:"),
    ("<piece> <piece # (ignore for queen/king)> <new position word> <new position number>"),
    ("For castles, the command would be: castle <rook number (1,2)>"),
    ("Example: soldier 4 dragon 4, queen expelliarmus 3, castle 2")
    ]
    multiRules = [
    ("Players' turns alternate, which is shown by the color of the boards."),
    ("White goes first, alternate making commands, and have fun!")
    ]
    cpuRules = [
    ("Turns alternate, which is shown by the color of the boards."),
    ("You are the white team, and the CPU is the black team. Have fun!")
    ]
    
    if data.prevMode == "multi":
        rules += multiRules
    elif data.prevMode == "cpu":
        rules += cpuRules
    
    x = data.width/2-70
    y = data.height/3-30
    for rule in rules:
        if ("IMPORTANT" in rule) or ('<' in rule) or ("before" in rule) or ("Example" in rule):
            color = "tomato"
            if ('<' in rule) or ("Example" in rule):
                f = "Hervetica 16 bold"
            else:
                f = "Hervetica 20 bold"
        else:
            color = "white"
            f = "Hervetica 20 bold"
        canvas.create_text(x,y, anchor=W, text=rule, fill=color, font=f)
        if rule.endswith("loading") or ('format' in rule) or ('<' in rule):
            y += 25
        else:
            y += 3 * data.cellSize / 4
       
    canvas.create_image(3*data.width/4 + 30,data.height/2-35, image=data.load)   
        
    ## KEY
    canvas.create_rectangle(data.margin/2-10, data.height/3-30, 5*data.width/12,
            5*data.height/6, outline="white", width=4)
    # piece key
    i = data.margin 
    j = data.height/3
    for piece in data.rulesPieces:
        canvas.create_image(i,j, image=piece.image)
        try: canvas.create_text(i+3,j+10, text=str(piece.number), fill="red",
                font="Arial 12 bold")
        except: pass
        canvas.create_text(i+data.cellSize, j, text=str(piece), fill="white",
                font="Hervetica 26 bold", anchor=W)
        j += data.cellSize
    # letter key
    m = data.width/4 
    n = data.height/3
    for letter in data.cols:
        canvas.create_text(m, n, text="%s - %s" %(letter[0], letter[1]), 
                font="Hervetica 26 bold", anchor=W, fill="white")
        n += 3 * data.cellSize / 4
        
    canvas.create_text(data.width/2, data.height-20, anchor=S, fill="bisque2",
                text="[ PRESS TAB TO GO BACK ]", font="Arial 30 bold")