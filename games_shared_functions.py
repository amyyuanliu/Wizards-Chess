import math
import copy
import speech_recognition as sr
from tkinter import *
from chess_classes import *
from speech_rec import *

# returns a list of the legal moves for a given piece and board
def pieceLegalMoves(data, piece):
    moves = []
    initPos = piece.position
    for row in range(8):
        for col in range(8):
            newPos = [row, col]
            if piece.checkSpace(data.board, newPos) and \
                    piece.isValidMove(data.board, newPos):
                data.board[initPos[0]][initPos[1]] = None
                piece.position = newPos
                curr = data.board[newPos[0]][newPos[1]]
                data.board[newPos[0]][newPos[1]] = piece
                if not inCheck(data):
                    moves.append(newPos)
                data.board[initPos[0]][initPos[1]] = piece
                data.board[newPos[0]][newPos[1]] = curr
                piece.position = initPos
    if moves == []:
        return None
    # 1st item in the list is the piece object itself
    return [piece] + moves


# returns a list of all legal moves for a player with a given board
def allLegalMoves(data):
    allMoves = []
    if data.whiteTurn:
        if isinstance(data.board[7][4], King) and not data.board[7][4].moved:
            if isinstance(data.board[7][0], Rook) and not data.board[7][0].moved and \
               data.board[7][1] == None and data.board[7][2] == None and \
               data.board[7][3] == None:
                allMoves.append("castle 1")
            if isinstance(data.board[7][7], Rook) and not data.board[7][7].moved and \
               data.board[7][6] == None and data.board[7][5] == None:
                allMoves.append("castle 2")
    else:
        if isinstance(data.board[0][4], King) and not data.board[0][4].moved:
            if isinstance(data.board[0][0], Rook) and not data.board[0][0].moved and \
               data.board[0][1] == None and data.board[0][2] == None and \
               data.board[0][3] == None:
                allMoves.append("castle 2")
            if isinstance(data.board[0][7], Rook) and not data.board[0][7].moved and \
               data.board[0][6] == None and data.board[0][5] == None:
                allMoves.append("castle 1")
    
    if data.whiteTurn:
        pieces = data.white
    else:
        pieces = data.black
    for piece in pieces:
        if pieceLegalMoves(data,piece) != None:
            allMoves.append(pieceLegalMoves(data,piece))
            
    return allMoves

# check for checkmate or stalemate
def checkEndGame(data):
    if allLegalMoves(data) == [] and inCheck(data):
        data.checkmate = True
    if allLegalMoves(data) == [] and not inCheck(data):
        data.stalemate = True

def castle(data, command):
    if len(command) != 2:
        data.tryAgain = True
        return
    # can't castle in check
    if data.check:
        data.falseMove = True
        return
    # get rook num
    n = None
    for i in data.num:
        if command[1] in i:
            n = data.num[i]
    if n == None:
        data.tryAgain = True
        return

    if data.whiteTurn:
        pieces = data.white
        other = data.black
    else:
        pieces = data.black
        other = data.white
    # check if king moved
    king = None
    for piece in pieces:
        if isinstance(piece, King):
            if piece.moved:
                data.falseMove = True
                return
            else:
                king = piece
            break
    # check if rook moved
    for piece in pieces:
        if isinstance(piece, Rook) and (piece.number == n):
            if piece.moved:
                data.falseMove = True
                return
            else:
                rook = piece
            
            # check if there are pieces in between
            r = rook.position
            k = king.position
            if r[1] < k[1]:
                for i in range(r[1]+1, k[1]):
                    if data.board[r[0]][i] != None:
                        data.falseMove = True
                        return
            if r[1] > k[1]:
                for i in range(k[1]+1, r[1]):
                    if data.board[r[0]][i] != None:
                        data.falseMove = True
                        return

            if data.whiteTurn and n == 1:
                rookPos = [7,2]
                kingPos = [7,1]
            elif data.whiteTurn and n == 2:
                rookPos = [7,5]
                kingPos = [7,6]
            elif not data.whiteTurn and n ==1:
                rookPos = [0,5]
                kingPos = [0,6]
            elif not data.whiteTurn and n == 2:
                rookPos = [0,2]
                kingPos = [0,1]
            # check for check in new position
            for opponent in other:
                if opponent.isValidMove(data.board, kingPos):
                    data.falseMove = True
                    return

            if rook.checkSpace(data.board, rookPos) and \
                king.checkSpace(data.board, kingPos):
                data.board[rook.position[0]][rook.position[1]] = None
                data.board[rookPos[0]][rookPos[1]] = rook
                rook.position = rookPos
                data.board[king.position[0]][king.position[1]] = None
                data.movingPiece = king
                data.moves = kingPos
    return 1

def takePiece(data, position):
    takenPiece = data.board[position[0]][position[1]]
    if data.whiteTurn:
        data.black.remove(takenPiece)
    else:
        data.white.remove(takenPiece)
    if takenPiece.team == "white":
        data.takenWhite.append(takenPiece)
    else:
        data.takenBlack.append(takenPiece)

def inCheck(data):
    if data.whiteTurn:
        target = data.white
        other = data.black
    else:
        target = data.black
        other = data.white
    # check if any piece in the opposing team can take the king
    for piece in target:
        if isinstance(piece, King):
            kingPos = piece.position
            break
    for piece in other:
        if piece.isValidMove(data.board, kingPos):
            return True
    return False

## white board
def drawWhiteBoard(canvas, data):
    if data.whiteTurn:
        hue = "sienna3"
        border = "brown"
    else:
        hue = "gray30"
        border = "gray15"
    board = [ ([None] * 8) for row in range(8) ]
    for row in range(8):
        for col in range(8):
            if (row%2 == 0 and col%2 == 0) or (row%2 == 1 and col%2 == 1):
                board[row][col] = ["white"]
            else:
                board[row][col] = [hue]
    for row in range(8):
        for col in range(8):
            left = col * data.cellSize + data.margin
            top = row * data.cellSize + data.margin + data.topScreen
            color = board[row][col]
            canvas.create_rectangle(left, top, left+data.cellSize,
                                        top+data.cellSize,
                                        fill=color, outline=border, width=4)

def drawWhiteBoardNumbers(canvas, data):
    for i in range(8):
        x = data.margin / 2
        y = 3* data.margin / 2 + data.cellSize * i + data.topScreen
        canvas.create_text(x, y, text=str(8-i), fill="white",
                            font="Arial 25 bold")
    for j in range(8):
        x = 3* data.margin / 2 + data.cellSize * j
        playHeight = 8 * data.cellSize + 2 * data.margin
        y = playHeight - data.margin / 2 + data.topScreen
        canvas.create_text(x, y, text=chr(ord('a')+ j), fill="white",
                            font="Arial 25 bold", anchor=S)

## black board
def drawBlackBoard(canvas, data):
    if data.whiteTurn:
        hue = "gray30"
        border = "gray15"
    else:
        hue = "sienna3"
        border = "brown"
    board = [ ([None] * 8) for row in range(8) ]
    for row in range(8):
        for col in range(8):
            if (row%2 == 0 and col%2 == 0) or (row%2 == 1 and col%2 == 1):
                board[row][col] = ["white"]
            else:
                board[row][col] = [hue]
    for row in range(8):
        for col in range(8):
            left = col * data.cellSize + data.margin + data.width/2
            top = row * data.cellSize + data.margin + data.topScreen
            color = board[row][col]
            canvas.create_rectangle(left, top, left+data.cellSize,
                                        top+data.cellSize,
                                        fill=color, outline=border, width=4)

def drawBlackBoardNumbers(canvas, data):
    for i in range(8):
        x = data.width - data.margin / 2
        y = 3* data.margin / 2 + data.cellSize * i + data.topScreen
        canvas.create_text(x, y, text=str(i+1), fill="white",
                            font="Arial 25 bold")
    for j in range(8):
        x = data.width/2 + 3* data.margin / 2 + data.cellSize * j
        playHeight = 8 * data.cellSize + 2 * data.margin
        y = playHeight - data.margin / 2 + data.topScreen
        canvas.create_text(x, y, text=chr(ord('h')- j), fill="white",
                            font="Arial 25 bold", anchor=S)
##

def drawPieces(canvas,data):
    if data.whiteTurn:
        for piece in data.black:
            piece.draw1(canvas, data.cellSize, data.margin, data.topScreen)
            piece.draw2(canvas, data.cellSize, data.margin, data.topScreen, data.width)

        for piece in data.white:
            piece.draw1(canvas, data.cellSize, data.margin, data.topScreen)
            piece.draw2(canvas, data.cellSize, data.margin, data.topScreen, data.width)

    else:
        for piece in data.white:
            piece.draw1(canvas, data.cellSize, data.margin, data.topScreen)
            piece.draw2(canvas, data.cellSize, data.margin, data.topScreen, data.width)

        for piece in data.black:
            piece.draw1(canvas, data.cellSize, data.margin, data.topScreen)
            piece.draw2(canvas, data.cellSize, data.margin, data.topScreen, data.width)

# type-in command box
def drawTextBox(canvas, data, lowerHeight):
    canvas.create_rectangle(data.width/2-300, data.height-lowerHeight/2-20,
            data.width/2+300, data.height-lowerHeight/2+20, fill="white", outline='gray')
    canvas.create_text(data.width/2, data.height-lowerHeight/2,
            text=data.command, font="Arial 26 bold")

def exit(canvas, data, playHeight):
    canvas.create_rectangle(data.width/2-200, playHeight/2-100,
        data.width/2+200, playHeight/2+100, fill='bisque2')
    canvas.create_text(data.width/2, playHeight/2-20,
        text="Are you sure you want to exit?", font="Hervetica 26 bold")
    canvas.create_rectangle(data.width/2-150, playHeight/2+40, data.width/2-30,
                    playHeight/2+70, outline="black")
    canvas.create_rectangle(data.width/2+30, playHeight/2+40, data.width/2+150,
                    playHeight/2+70, outline="black")
    canvas.create_text(data.width/2-90, playHeight/2+55, text="YES",
                font="Hervetica 16 bold")
    canvas.create_text(data.width/2+90, playHeight/2+55, text="NO",
                font="Hervetica 16 bold")
