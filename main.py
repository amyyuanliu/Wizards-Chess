import math
import copy
import speech_recognition as sr
from tkinter import *
# import files
from chess_classes import *
from start_screen import *
from speech_rec import *
from multi_mode import *
from cpu_mode import *
from end_screen import *
from rules_screen import *
from games_shared_functions import *


def init(data):
    ## START SCREEN
    data.mode = "start"
    data.logo = PhotoImage(file='images/logo.gif')
    data.background = PhotoImage(file='images/HP_Background.gif')
    data.xSize = 150
    data.ySize = 30
    data.king = PhotoImage(file='images/chess_pieces.gif')
    data.fawks = PhotoImage(file='images/fawks.gif')
    ## RULES SCREENS
    initRulesPieces(data)
    data.load = PhotoImage(file='images/load.gif')
    data.prevMode = None
    ## GAME MODES
    # display stuff
    data.timer = 0
    data.broomstick = PhotoImage(file='images/broomstick.gif')
    data.platform = PhotoImage(file='images/platform.gif')
    data.board = [ ([None] * 8) for row in range(8) ]
    data.margin = 63
    data.topScreen = 60
    data.cellSize = 62
    # chess pieces from their classes
    initBlack(data)
    initWhite(data)
    # algorithm data variables
    data.takenBlack = []
    data.takenWhite = []
    data.movingPiece = None
    data.moves = None
    data.check = False
    data.tryAgain = False
    data.falseMove = False
    data.checkmate = False
    data.stalemate = False
    data.type = False # if user wants to type command instead
    data.command = ""
    data.whiteTurn = True # alternate between black/white team
    # dictionaries for translation of commands
    data.rows = {('8','eight','ate'):0, 
                  ('7','seven'):1, 
                  ('6','six'):2, 
                  ('5','five', 'spy'):3, 
                  ('4','four','for'):4, 
                  ('3','three'):5, 
                  ('2','two', 'to','too'):6, 
                  ('1','one','won','juan'):7}
    data.cols = {('a','astronomy'):0, ('b','butterbeer'):1, ('c','charms','charm'):2, 
                ('d','dragon'):3, ('e','expelliarmus'):4, ('f','fawks','fox'):5, 
                ('g','goblin', 'auburn'):6, ('h','hogwarts'):7}
    data.translate = {('soldier', 'pawn'):Pawn, ('knight',"night"):Knight, 
                ('bishop','up'):Bishop, ('king','key'):King, ('queen','q'):Queen, 
                ("rook",'rock', 'rogue', 'brooke', 'brook'):Rook}
    data.num = {('8','eight','ate'):8, 
                  ('7','seven'):7, 
                  ('6','six'):6, 
                  ('5','five'):5, 
                  ('4','four','for'):4, 
                  ('3','three'):3, 
                  ('2','two', 'to','too'):2, 
                  ('1','one','won','juan'):1}
    data.exitRequest = False
    data.exit = False
    
# piece commands examples for the rules
def initRulesPieces(data):
    data.rulesPieces = []
    data.rulesPieces.append(Pawn(4, [0,0], "white"))
    data.rulesPieces.append(Knight(1, [0,0], "black"))
    data.rulesPieces.append(Bishop(2, [0,0], "white"))
    data.rulesPieces.append(Rook(1, [0,0], "black"))
    data.rulesPieces.append(Queen([0,0], "white"))
    data.rulesPieces.append(King([0,0], "black"))
    
    
# initialize the black pieces
# Piece(number if applicable, position, team)  
def initBlack(data):
    data.black = []
    for i in range(8):
        data.black.append(Pawn(8-i, [1,i], "black"))
    data.black.append(Bishop(2, [0,2], "black"))
    data.black.append(Bishop(1, [0,5], "black"))
    data.black.append(Rook(2, [0,0], "black"))
    data.black.append(Rook(1, [0,7], "black"))
    data.black.append(King([0,4], "black"))
    data.black.append(Queen([0,3], "black"))
    data.black.append(Knight(2, [0,1], "black"))
    data.black.append(Knight(1, [0,6], "black"))
    for piece in data.black:
        row = piece.position[0]
        col = piece.position[1]
        data.board[row][col] = piece

# initialize the white pieces 
# Piece(number if applicable, position, team)   
def initWhite(data):
    data.white = []
    for i in range(8):
        data.white.append(Pawn(i+1, [6,i], "white"))
    data.white.append(Bishop(1, [7,2], "white"))
    data.white.append(Bishop(2, [7,5], "white"))
    data.white.append(Rook(1, [7,0], "white"))
    data.white.append(Rook(2, [7,7], "white"))
    data.white.append(King([7,4], "white"))
    data.white.append(Queen([7,3], "white"))
    data.white.append(Knight(1, [7,1], "white"))
    data.white.append(Knight(2, [7,6], "white"))
    for piece in data.white:
        row = piece.position[0]
        col = piece.position[1]
        data.board[row][col] = piece


def mousePressed(event, data):
    if (data.mode == "start"): startMousePressed(event, data)
    elif (data.mode == "rules"): rulesMousePressed(event, data)
    elif (data.mode == "multi"): multiMousePressed(event, data)
    elif (data.mode == "cpu"): cpuMousePressed(event, data)
    elif (data.mode == "end"): endMousePressed(event, data)
    

def keyPressed(event, data):
    # shortcut to end screen for demonstration
    if event.keysym == "Up":
        data.mode = "end"
    elif (data.mode == "start"): startKeyPressed(event, data)
    elif (data.mode == "rules"): rulesKeyPressed(event, data)
    elif (data.mode == "multi"): multiKeyPressed(event, data)
    elif (data.mode == "cpu"): cpuKeyPressed(event, data)
    elif (data.mode == "end"): 
        if event.keysym == "space":
            init(data) 
    
def timerFired(data):
    # exit game
    if data.exit:
        init(data)
    if (data.mode == "start"): startTimerFired(data)
    elif (data.mode == "rules"): rulesTimerFired(data)
    elif (data.mode == "multi"): multiTimerFired(data)
    elif (data.mode == "cpu"): cpuTimerFired(data)
    elif (data.mode == "end"): endTimerFired(data)
    
def redrawAll(canvas, data):
    if (data.mode == "start"): startRedrawAll(canvas, data)
    elif (data.mode == "rules"): rulesRedrawAll(canvas, data)
    elif (data.mode == "multi"): multiRedrawAll(canvas, data)
    elif (data.mode == "cpu"): cpuRedrawAll(canvas, data)
    elif (data.mode == "end"): endRedrawAll(canvas, data)
    

    
# SOURCE: 15-112 website course notes
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
#####

def play():
    cellSize = 63
    topScreen = 60
    bottomScreen = 60
    margin = 60
    width = 16* cellSize + 4 * margin
    height = 8 * cellSize + 2 * margin + bottomScreen + topScreen
    run(width, height)


play()
