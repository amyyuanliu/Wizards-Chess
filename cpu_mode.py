import math
import copy
import speech_recognition as sr
from tkinter import *
from chess_classes import *
from speech_rec import *
from games_shared_functions import *

# function to evaluate board for AI using the tables in the piece classes
def evaluate(board):
    eval = 0
    for row in range(8):
        for col in range(8):
            if isinstance(board[row][col], ChessPiece):
                piece = board[row][col]
                eval += (piece.value + piece.posVal[row][col])
    return eval

# make move for backtracking
def makeMove(data, p, move):
    if data.whiteTurn:
        pieces = data.white
    else:
        pieces = data.black
    i = pieces.index(p)
    piece = pieces[i]
    data.board[piece.position[0]][piece.position[1]] = None
    piece.position = move
    if data.board[move[0]][move[1]] != None:
        takePiece(data, move)
    data.board[move[0]][move[1]] = piece
    data.whiteTurn = not data.whiteTurn

# backtracking minimax w/ alpha beta pruning
def minimax(data, depth, alpha, beta):
    if depth == 0 or data.checkmate or data.stalemate:
        return (evaluate(data.board), None, None)
    else:
        if not data.whiteTurn:
            bestMove = None
            bestPiece = None
            bestScore = float("inf") 
            for pieceMoves in allLegalMoves(data):
                if "castle" in pieceMoves:
                    continue
                piece = pieceMoves[0]
                for move in pieceMoves[1:]:
                    # store values to restore when undoing the move
                    initPos = piece.position
                    curr = data.board[move[0]][move[1]]
                    if curr != None:
                        i = data.white.index(curr)
                    turn = data.whiteTurn
                    makeMove(data, piece, move)
                    score, p, m = minimax(data, depth-1, alpha, beta)
                    #undo move
                    data.board[initPos[0]][initPos[1]] = piece
                    data.board[move[0]][move[1]] = curr
                    if curr != None and curr not in data.white:
                        if isinstance(curr, Knight):
                            data.white.append(curr)
                        else:
                            data.white.insert(i, curr)
                    piece.position = initPos
                    data.whiteTurn = turn
                    # compare the moves to find best one
                    if score < bestScore:
                        bestScore = score
                        bestMove = move
                        bestPiece = piece
                        beta = min(beta, bestScore)
                        if (alpha >= beta):
                            return (bestScore, bestPiece, bestMove)
        else:
            bestMove = None
            bestScore = -float("inf") 
            bestPiece = None
            for pieceMoves in allLegalMoves(data):
                if "castle" in pieceMoves:
                    continue
                piece = pieceMoves[0]
                for move in pieceMoves[1:]:
                    initPos = piece.position
                    curr = data.board[move[0]][move[1]]
                    if curr != None:
                        i = data.black.index(curr)
                    turn = data.whiteTurn
                    makeMove(data, piece, move)
                    score, p, m = minimax(data, depth-1, alpha, beta)
                    #undo move
                    data.board[initPos[0]][initPos[1]] = piece
                    data.board[move[0]][move[1]] = curr
                    if curr != None and curr not in data.black:
                        if isinstance(curr, Knight):
                            data.black.append(curr)
                        else:
                            data.black.insert(i, curr)
                    piece.position = initPos
                    data.whiteTurn = turn
                    if score > bestScore:
                        bestScore = score
                        bestMove = move
                        bestPiece = piece
                        alpha = max(alpha, bestScore)
                        if (alpha >= beta):
                            return (bestScore, bestPiece, bestMove)
        return (bestScore, bestPiece, bestMove)

def getBestMove(data):
    # prioritize castles
    if "castle 1" in allLegalMoves(data)[:2]:
        return "castle 1"
    if "castle 2" in allLegalMoves(data)[:2]:
        return "castle 2"
    return minimax(data, 3, -float("inf"), float("inf"))

# create CPU command
def moveCPU(data):
    if "castle" in getBestMove(data):
        return getBestMove(data)
    move = getBestMove(data)[2]
    piece = getBestMove(data)[1]
    try: num = str(piece.number)
    except: num = ""
    for p in data.translate:
        if isinstance(piece, data.translate[p]):
            piece = p[0]
            break
    for i in data.cols:
        if data.cols[i] == move[1]:
            col = i[0]
            break
    row = str(8-move[0])
    command = piece+" "+num+" "+col+" "+row
    return command

        
def cpuMousePressed(event, data):
    playHeight = 8 * data.cellSize + 2 * data.margin + data.topScreen
    if data.whiteTurn and not (data.checkmate or data.stalemate):
        lowerHeight = (data.height-(playHeight-data.margin/2))
        if (data.width/2 - 300 < event.x < data.width/2 + 300) and \
            (data.height-lowerHeight/2-20 < event.y < data.height-lowerHeight/2+20):
            data.type = True
    if data.exitRequest and playHeight/2+40 < event.y < playHeight/2+70:
        if data.width/2-150 < event.x < data.width/2-30:
            data.exit = True
        elif data.width/2+30 < event.x <data.width/2+150:
            data.exitRequest = False
    if 20 < event.x < 140 and 50 < event.y < 90:
        data.mode = "rules"   


def cpuTimerFired(data):
    if not (data.checkmate or data.stalemate):
        data.timer += 1
    if not (data.checkmate or data.stalemate):
        if data.movingPiece != None:
            data.movingPiece.moveAnimation(data.moves)
            if data.movingPiece.position == data.moves:
                if data.board[data.moves[0]][data.moves[1]] != None:
                    takePiece(data, data.moves)
                data.board[data.moves[0]][data.moves[1]] = data.movingPiece
                data.whiteTurn = not data.whiteTurn
                data.movingPiece = None
                data.moves = None
                if inCheck(data):
                    data.check = True
                else:
                    data.check = False
                checkEndGame(data)
                if not data.whiteTurn:
                    movePiece(data, moveCPU(data))
    

# command:
# <piece in lowercase> <piece number if applicable> <letter lowercase> <num>
def movePiece(data, command):
    if command == None:
        data.tryAgain = True
        return

    command = command.lower()
    print(command)
    command = command.strip().split(" ")

    #CASTLE
    if "castle" in command:
        castle(data, command)
        return

    # break down the command
    if len(command) == 4:
        letter = command[2]
        num = command[3]
    # King, Queen
    elif len(command) == 3:
        letter = command[1]
        num = command[2]
    else:
        data.tryAgain = True
        return

    # get the piece
    pieceType = None
    for piece in data.translate:
        if command[0] in piece:
            pieceType = data.translate[piece]
    if pieceType == None:
        data.tryAgain = True
        return

    # get the new position
    newPos = [None, None]
    for y in data.rows:
        if num in y:
            newPos[0] = data.rows[y]
    for x in data.cols:
        if letter in x:
            newPos[1] = data.cols[x]
    if None in newPos:
        data.tryAgain = True
        return

    # get the piece number
    if not (pieceType == King or pieceType == Queen):
        n = None
        for i in data.num:
            if command[1] in i:
                n = data.num[i]
        if n == None:
            data.tryAgain = True
            return

    if data.whiteTurn:
        pieces = data.white
    else:
        pieces = data.black

    for piece in pieces:
        try: checkPieceNum = (piece.number == n)
        except: checkPieceNum = True # Queen, King
        if isinstance(piece, pieceType) and checkPieceNum:
            if piece.checkSpace(data.board, newPos) and \
                    piece.isValidMove(data.board, newPos):
                if data.whiteTurn:
                    # check for check
                    initPos = piece.position
                    data.board[initPos[0]][initPos[1]] = None
                    piece.position = newPos
                    curr = data.board[newPos[0]][newPos[1]]
                    if curr != None:
                        takePiece(data, newPos)
                    data.board[newPos[0]][newPos[1]] = piece
                    if inCheck(data):
                        data.board[initPos[0]][initPos[1]] = piece
                        data.board[newPos[0]][newPos[1]] = curr
                        piece.position = initPos
                        if curr != None and data.whiteTurn:
                            if isinstance(curr, Knight):
                                data.black.append(curr)
                            else:
                                data.black.insert(0, curr)
                        elif curr != None and not data.whiteTurn:
                            if isinstance(curr, Knight):
                                data.white.append(curr)
                            else:
                                data.white.insert(0, curr)
                        data.falseMove = True
                        print("INVALID MOVE: in check")
                    else:
                        # undo moves
                        data.board[newPos[0]][newPos[1]] = curr
                        piece.position = initPos
                        if curr != None and data.whiteTurn:
                            if isinstance(curr, Knight):
                                data.black.append(curr)
                            else:
                                data.black.insert(0, curr)
                        elif curr != None and not data.whiteTurn:
                            if isinstance(curr, Knight):
                                data.white.append(curr)
                            else:
                                data.white.insert(0, curr)
                        data.falseMove = False
                        data.movingPiece = piece
                        data.moves = newPos
                        piece.moved = True
                else:
                    data.board[piece.position[0]][piece.position[1]] = None
                    data.falseMove = False
                    data.movingPiece = piece
                    data.moves = newPos
                    piece.moved = True
            else:
                data.falseMove = True
                print("INVALID MOVE")
            return
    data.falseMove = True
    print("INVALID MOVE")
            
def cpuKeyPressed(event, data):
    if event.keysym == "Escape":
        data.exitRequest = True
    if data.whiteTurn and not (data.checkmate or data.stalemate):
        if data.type:
            data.tryAgain = False
            if event.char.isalnum():
                data.command += event.char
            elif event.keysym == "BackSpace":
                data.command = data.command[:-1]
            elif event.keysym == "space":
                data.command += event.char
            elif event.keysym == "Return":
                movePiece(data, data.command)
                data.command = ""
                data.type = False
            elif event.keysym == "Tab":
                data.command = ""
                data.type = False
                
        elif event.keysym == "space":
            data.tryAgain = False
            command = speechToText(sr.Recognizer(), sr.Microphone())["transcription"]
            movePiece(data, command)
    else:
        if event.keysym == "Return":
            data.mode = "end"
            

def cpuRedrawAll(canvas, data):
    playHeight = 8 * data.cellSize + 2 * data.margin + data.topScreen
    canvas.create_image(0,0, image=data.background, anchor=NW)
    canvas.create_image(data.width/2, data.topScreen + 10, image=data.logo)
    canvas.create_text(data.width-data.margin,60, text="CPU", font="Arial 50 bold", 
                                            fill="brown", anchor=NE)
    drawWhiteBoard(canvas,data)
    drawWhiteBoardNumbers(canvas,data)
    drawBlackBoard(canvas, data)
    drawBlackBoardNumbers(canvas, data)
    drawPieces(canvas, data)
    canvas.create_image(data.width/2, playHeight/2+20, image=data.broomstick)
    canvas.create_image(data.width/2, playHeight/2+30, image=data.platform)
    # bottom rectangle
    canvas.create_rectangle(0,playHeight-data.margin/2, data.width, data.height, 
                            fill="bisque2", outline="")
    lowerHeight = (data.height-(playHeight-data.margin/2))
    # textbox
    if not (data.checkmate or data.stalemate):
        drawTextBox(canvas, data, lowerHeight)
    # check, falsemove, tryagain
    if data.check or data.falseMove or data.tryAgain:
        if data.whiteTurn:
            canvas.create_rectangle(10, data.height-lowerHeight/2-20, 210,
                        data.height-lowerHeight/2+20, fill="red", outline="")
            if data.check:
                canvas.create_text(110, data.height-lowerHeight/2, text="CHECK",
                                font="Arial 26 bold", fill="white")
            elif data.falseMove:
                canvas.create_text(110, data.height-lowerHeight/2, text="INVALID MOVE",
                                font="Arial 22 bold", fill="white")
            else:
                canvas.create_text(110, data.height-lowerHeight/2, text="TRY AGAIN",
                                font="Arial 24 bold", fill="white")
        else:
            canvas.create_rectangle(data.width-10, data.height-lowerHeight/2-20,
                        data.width-210, data.height-lowerHeight/2+20, 
                        fill="red", outline="")
            canvas.create_text(data.width-110, data.height-lowerHeight/2, 
                    text="CHECK", font="Arial 26 bold", fill="white")
    # checkmate
    if data.checkmate:
        if data.whiteTurn:
            team = "Black"
        else:
            team = "White"
        canvas.create_text(data.width/2, data.height-lowerHeight/2, 
            text = "Checkmate! " + team + " team wins.", font="Arial 26 bold")
        canvas.create_text(data.width/2, data.height-lowerHeight/2 + 26,
            text = "press [ ENTER ] to continue", font="Arial 22 bold")
    # stalemate
    if data.stalemate:
        canvas.create_text(data.width/2, data.height-lowerHeight/2, 
            text = "Stalemate! The game is a draw.", font="Arial 26 bold")
        canvas.create_text(data.width/2, data.height-lowerHeight/2 + 26,
            text = "press [ ENTER ] to continue", font="Arial 22 bold")
    # escape
    canvas.create_text(20, 20, text="[ ESC ]", fill="white", anchor=NW,
                font="Arial 16 bold")
    if data.exitRequest:
        exit(canvas, data, playHeight)
    
    # rules
    canvas.create_rectangle(20, 50, 140, 90, fill="bisque2", outline="white", width=2)
    canvas.create_text(30, 50, text="RULES", anchor=NW, font="Arial 30 bold")