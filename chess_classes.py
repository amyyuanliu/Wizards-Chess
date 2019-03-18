from tkinter import *
import math
import copy

# base chess piece class
class ChessPiece(object):
    def __init__(self, number, position, team):
        self.number = number     # i.e. knight 1 or knight 2
        self.position = position # place on the board
        self.team = team         # black or white

    def __hash__(self):
        return hash(type(self), self.number)

    # draw pieces for 1st board (white)
    def draw1(self, canvas, cellSize, margin, top):
        x = self.position[1] * cellSize + margin + cellSize/2
        y = self.position[0] * cellSize + margin + cellSize/2 + top
        canvas.create_image(x,y, image=self.image)
        try: canvas.create_text(x+3,y+10, text=str(self.number), fill="red",
                    font="Arial 12 bold")
        except: pass

    # draw pieces for 2nd board (black)
    def draw2(self, canvas, cellSize, margin, top, width):
        x = (7-self.position[1]) * cellSize + margin + cellSize/2 + width/2
        y = (7-self.position[0]) * cellSize + margin + cellSize/2 + top
        canvas.create_image(x,y, image=self.image)
        try: canvas.create_text(x+3,y+10, text=str(self.number), fill="red",
                    font="Arial 12 bold")
        except: pass

    # for moves, checks if new position is taken up by piece of own team
    def checkSpace(self, board, newPos):
        if isinstance(board[newPos[0]][newPos[1]], ChessPiece):
            if board[newPos[0]][newPos[1]].team == self.team:
                return False
        return True


    # include in base class so Queen subclass can use it
    def rookIsValid(self, board, newPos):
        # vertical move
        case1 = (newPos[0] != self.position[0]) and \
                (newPos[1] == self.position[1])
        # horizontal move
        case2 = (newPos[0] == self.position[0]) and \
                (newPos[1] != self.position[1])

        if case1:
            # check if there are any pieces in between old and new position
            if (newPos[0] < self.position[0]):
                for i in range(1, self.position[0]-newPos[0]):
                    if board[self.position[0]-i][self.position[1]] != None:
                        return False
            else:
                for i in range(1, newPos[0]-self.position[0]):
                    if board[self.position[0]+i][self.position[1]] != None:
                        return False
            return True

        elif case2:
            # check if there are any pieces in between old and new position
            if (newPos[1] < self.position[1]):
                for i in range(1, self.position[1]-newPos[1]):
                    if board[self.position[0]][self.position[1]-i] != None:
                        return False
            else:
                for i in range(1, newPos[1]-self.position[1]):
                    if board[self.position[0]][self.position[1]+i] != None:
                        return False
            return True

        else:
            return False

    # include in base class so Queen subclass can use it
    def bishopIsValid(self, board, newPos):
        case = (abs(newPos[0]-self.position[0]) ==
                abs(newPos[1]-self.position[1]))

        if case:
            row1 = newPos[0]
            row0 = self.position[0]
            col1 = newPos[1]
            col0 = self.position[1]

            # check if there are any pieces in between old and new position
            if (row1 < row0) and (col1 < col0):
                for i in range(1, row0-row1):
                    if board[row0-i][col0-i] != None:
                         return False

            elif (row1 < row0) and (col1 > col0):
                for i in range(1, row0-row1):
                    if board[row0-i][col0+i] != None:
                        return False

            elif (row1 > row0) and (col1 < col0):
                for i in range(1, row1-row0):
                    if board[row0+i][col0-i] != None:
                        return False

            elif (row1 > row0) and (col1 > col0):
                for i in range(1, row1-row0):
                    if board[row0+i][col0+i] != None:
                        return False
            return True

        else:
            return False

    # for piece to drift accross the board during moves
    def moveAnimation(self, newPos):
        if newPos[0] < self.position[0]:
            vStep = -0.1
        elif newPos[0] > self.position[0]:
            vStep = 0.1
        else: # newPos[0] == self.position[0]
            vStep = 0

        if newPos[1] < self.position[1]:
            hStep = -0.1
        elif newPos[1] > self.position[1]:
            hStep = 0.1
        else: # newPos[1] == self.position[1]
            hStep = 0

        if abs(newPos[0] - self.position[0]) >= 0.1 or \
            abs(newPos[1] - self.position[1]) >= 0.1:
            self.position[0] += vStep
            self.position[1] += hStep
        else:
            self.position = newPos


class Pawn(ChessPiece):
    def __init__(self, number, position, team):
        super().__init__(number, position, team)
        self.moved = False
        self.table = [
                    [ 0,  0,  0,  0,  0,  0,  0,  0],
                    [ 5,  5,  5,  5,  5,  5,  5,  5],
                    [ 1,  1,  2,  3,  3,  2,  1,  1],
                    [.5, .5,  1,2.7,2.7,  1, .5, .5],
                    [ 0,  0,  0,2.5,2.5,  0,  0,  0],
                    [.5,-.5, -1,  0,  0, -1,-.5, .5],
                    [.5,  1,  1,-2.5,-2.5, 1, 1, .5],
                    [ 0,  0,  0,  0,  0,  0,  0,  0]   ]
        if team == "black":
            self.image = PhotoImage(file='pieces/blackPawn.gif')
            self.value = -10 # for CPU game AI algorithm
            self.posVal = [ ([0] * 8) for row in range(8) ]
            for i in range(8):
                for j in range(8):
                    self.posVal[i][j] = -self.table[7-i][7-j]

        elif team == "white":
            self.image = PhotoImage(file="pieces/whitePawn.gif")
            self.value = 10
            self.posVal = copy.deepcopy(self.table)

    def __repr__(self):
        return "soldier " + str(self.number)

    def isValidMove(self, board, newPos):
        if self.position == newPos:
            return False

        if self.team == "black":
            # move forward to blank space
            case1 = (newPos[0] == self.position[0]+1) and \
                    (newPos[1] == self.position[1]) and\
                    board[newPos[0]][newPos[1]] == None
            # move diagonal to take a piece
            case2 = (newPos[0] == self.position[0]+1) and \
                    (newPos[1] == self.position[1]+1 or
                        newPos[1] == self.position[1]-1)  and \
                    board[newPos[0]][newPos[1]] != None
            # move forward 2 spots if in initial position
            startCase = (self.position[0] == 1) and (newPos[0] == 3) and \
                        (newPos[1] == self.position[1]) and \
                        (board[newPos[0]][newPos[1]] == None) and \
                        (board[newPos[0]-1][newPos[1]] == None)

        elif self.team == "white":
            # move forward to blank space
            case1 = (newPos[0] == self.position[0]-1) and \
                    (newPos[1] == self.position[1]) and\
                    board[newPos[0]][newPos[1]] == None
            # move diagonal to take a piece
            case2 = (newPos[0] == self.position[0]-1) and \
                    (newPos[1] == self.position[1]+1 or
                        newPos[1] == self.position[1]-1) and \
                    board[newPos[0]][newPos[1]] != None
            # move forward 2 spots if in initial position
            startCase = (self.position[0] == 6) and (newPos[0] == 4) and \
                        (newPos[1] == self.position[1]) and \
                        (board[newPos[0]][newPos[1]] == None) and \
                        (board[newPos[0]+1][newPos[1]] == None)

        if case1 or case2 or startCase:
            return True
        else:
            return False


class Knight(ChessPiece):
    def __init__(self, number, position, team):
        super().__init__(number, position, team)
        self.moved = False
        self.table = [
                    [ -5, -4, -3, -3, -3, -3, -4, -5],
                    [ -4, -2,  0,  0,  0,  0, -2, -4],
                    [ -3,  0,  1,1.5,1.5,  1,  0, -3],
                    [ -3, .5,1.5,  2,  2,1.5, .5, -3],
                    [ -3,  0,1.5,  2,  2,1.5,  0, -3],
                    [ -3, .5,  1,1.5,1.5,  1, .5, -3],
                    [ -4, -2,  0, .5, .5,  0, -2, -4],
                    [ -5, -4, -2, -3, -3, -2, -4, -5]
                    ]
        if team == "black":
            self.image = PhotoImage(file='pieces/blackKnight.gif')
            self.value = -30
            self.posVal = [ ([0] * 8) for row in range(8) ]
            for i in range(8):
                for j in range(8):
                    self.posVal[i][j] = -self.table[7-i][7-j]
        elif team == "white":
            self.image = PhotoImage(file='pieces/whiteKnight.gif')
            self.value = 30
            self.posVal = copy.deepcopy(self.table)

    def __repr__(self):
        return "knight " + str(self.number)

    def isValidMove(self, board, newPos):
        if self.position == newPos:
            return False

        # vertical = 2, horizontal = 1
        case1 =  (abs(newPos[0]-self.position[0]) == 2) and \
                (abs(newPos[1]-self.position[1]) == 1)
        # vertical = 1, horizontal = 1
        case2 = (abs(newPos[0]-self.position[0]) == 1) and \
                (abs(newPos[1]-self.position[1]) == 2)
        if case1 or case2:
            return True
        else:
            return False

    # override base function because knight moves differently
    def moveAnimation(self, newPos):
        if newPos[1] < self.position[1]:
            hStep = -0.1
        else:
            hStep = 0.1

        if newPos[0] < self.position[0]:
            vStep = -0.1
        else:
            vStep = 0.1

        # first vertical move
        if abs(self.position[0] - newPos[0]) >= 0.1:
            self.position[0] += vStep
        else:
            self.position[0] = newPos[0]

        # horizontal move
        if self.position[0] == newPos[0]:
            if abs(self.position[1] - newPos[1]) >= 0.1:
                self.position[1] += hStep
            else:
                self.position = newPos


class Queen(ChessPiece):
    def __init__(self, position, team):
        self.position = position
        self.team = team
        self.moved = False
        self.table = [
                    [ -2, -1, -1,-.5,-.5, -1, -1, -2],
                    [ -1,  0,  0,  0,  0,  0,  0, -1],
                    [ -1,  0, .5, .5, .5, .5,  0, -1],
                    [ -.5,  0, .5, .5, .5, .5, 0,-.5],
                    [  0,  0, .5, .5, .5, .5,  0,-.5],
                    [ -1, .5, .5, .5, .5, .5,  0, -1],
                    [ -1,  0, .5,  0,  0,  0,  0, -1],
                    [ -2, -1, -1,-.5,-.5, -1, -1, -2]
                ]
        if team == "black":
            self.image = PhotoImage(file='pieces/blackQueen.gif')
            self.value = -90
            self.posVal = [ ([0] * 8) for row in range(8) ]
            for i in range(8):
                for j in range(8):
                    self.posVal[i][j] = -self.table[7-i][7-j]
        elif team == "white":
            self.image = PhotoImage(file='pieces/whiteQueen.gif')
            self.value = 90
            self.posVal = copy.deepcopy(self.table)

    def __repr__(self):
        return "queen"

    def isValidMove(self, board, newPos):
        if self.position == newPos:
            return False

        # Queen's moves consist of rook's moves and bishop's moves
        if self.rookIsValid(board, newPos):
            return True
        elif self.bishopIsValid(board, newPos):
            return True
        else:
            return False

class King(ChessPiece):
    def __init__(self, position, team):
        self.position = position
        self.team = team
        self.moved = False
        self.table = [
                    [ -3, -4, -4, -5, -5, -4, -4, -3],
                    [ -3, -4, -4, -5, -5, -4, -4, -3],
                    [ -3, -4, -4, -5, -5, -4, -4, -3],
                    [ -3, -4, -4, -5, -5, -4, -4, -3],
                    [ -2, -3, -3, -4, -4, -3, -3, -2],
                    [ -1, -2, -2, -2, -2, -2, -2, -1],
                    [  2,  2,  0,  0,  0,  0,  2,  2],
                    [  2,  3,  1,  0,  0,  1,  3,  2]
                    ]
        if team == "black":
            self.image = PhotoImage(file='pieces/blackKing.gif')
            self.value = -900
            self.posVal = [ ([0] * 8) for row in range(8) ]
            for i in range(8):
                for j in range(8):
                    self.posVal[i][j] = -self.table[7-i][7-j]
        elif team == "white":
            self.image = PhotoImage(file='pieces/whiteKing.gif')
            self.value = 900
            self.posVal = copy.deepcopy(self.table)

    def __repr__(self):
        return "king"

    def isValidMove(self, board, newPos):
        if self.position == newPos:
            return False

        case = (abs(newPos[0] - self.position[0]) <= 1) and \
                (abs(newPos[1] - self.position[1]) <= 1)
        if case:
            return True
        else:
            return False


class Bishop(ChessPiece):
    def __init__(self, number, position, team):
        super().__init__(number, position, team)
        self.moved = False
        self.table = [
                    [ -2, -1, -1, -1, -1, -1, -1, -2],
                    [ -1,  0,  0,  0,  0,  0,  0, -1],
                    [ -1,  0, .5,  1,  1, .5,  0, -1],
                    [ -1, .5, .5,  1,  1, .5, .5, -1],
                    [ -1,  0,  1,  1,  1,  1,  0, -1],
                    [ -1,  1,  1,  1,  1,  1,  1, -1],
                    [ -1, .5,  0,  0,  0,  0, .5, -1],
                    [ -2, -1, -4, -1, -1, -4, -1, -2]
                    ]
        if team == "black":
            self.image = PhotoImage(file='pieces/blackBishop.gif')
            self.value = -30
            self.posVal = [ ([0] * 8) for row in range(8) ]
            for i in range(8):
                for j in range(8):
                    self.posVal[i][j] = -self.table[7-i][7-j]
        elif team == "white":
            self.image = PhotoImage(file='pieces/whiteBishop.gif')
            self.value = 30
            self.posVal = copy.deepcopy(self.table)

    def __repr__(self):
        return "bishop " + str(self.number)

    def isValidMove(self, board, newPos):
        if self.position == newPos:
            return False

        return self.bishopIsValid(board, newPos)


class Rook(ChessPiece):
    def __init__(self, number, position, team):
        super().__init__(number, position, team)
        self.moved = False
        self.table = [
                    [  0,  0,  0,  0,  0,  0,  0,  0],
                    [ .5,  1,  1,  1,  1,  1,  1, .5],
                    [-.5,  0,  0,  0,  0,  0,  0,-.5],
                    [-.5,  0,  0,  0,  0,  0,  0,-.5],
                    [-.5,  0,  0,  0,  0,  0,  0,-.5],
                    [-.5,  0,  0,  0,  0,  0,  0,-.5],
                    [-.5,  0,  0,  0,  0,  0,  0,-.5],
                    [  0,  0,  0, .5, .5,  0,  0,  0],
        ]
        if team == "black":
            self.image = PhotoImage(file='pieces/blackRook.gif')
            self.value = -50
            self.posVal = [ ([0] * 8) for row in range(8) ]
            for i in range(8):
                for j in range(8):
                    self.posVal[i][j] = -self.table[7-i][7-j]
        elif team == "white":
            self.image = PhotoImage(file='pieces/whiteRook.gif')
            self.value = 50
            self.posVal = copy.deepcopy(self.table)
            
    def __repr__(self):
        return "rook " + str(self.number)

    def isValidMove(self, board, newPos):
        if self.position == newPos:
            return False

        elif self.rookIsValid(board, newPos):
            return True

        return False

"""
self.table values are used for the evaluation function for the cpu minimax
function, and the values were obtained through research mainly from:
http://www.chessbin.com/post/Chess-Board-Evaluation
with a few adjustments
"""
