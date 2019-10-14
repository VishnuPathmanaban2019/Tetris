#################################################
# Developer: Vishnu Pathmanaban
# Email: vpathman@andrew.cmu.edu
# Start Date: 10/11/2019
# Last Updated: 10/12/2019
# Title: Recreation of Tetris (CMU 15-112)
# Notes:
# - up arrow key to rotate piece
# - left and right arrow keys to move piece
# - down arrow key to hard drop piece
# (Tetris is a game published by Tengen under Atari Games)
#################################################

import cs112_f19_week7_linter
import math, copy, random

from cmu_112_graphics import *
from tkinter import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

#defines game dimensions
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return(rows,cols,cellSize,margin)

#runs Tetris game app with set dimensions
def playTetris():
    rows,cols,cellSize,margin = gameDimensions()
    width = cols*cellSize+margin*2
    height = rows*cellSize+margin*2
    runApp(width=width, height=height)

#model for Tetris game app
def appStarted(app):
    app.rows,app.cols,app.cellSize,app.margin = gameDimensions()
    app.board = []
    for i in range(app.rows):
        app.board.append([])
        for j in range(app.cols):
            app.board[i].append('blue')
    app.fullRows=[]
    app.score=0
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],[  True,  True,  True ]]
    lPiece = [[ False, False,  True ],[  True,  True,  True ]]
    oPiece = [[  True,  True ],[  True,  True ]]
    sPiece = [[ False,  True,  True ],[  True,  True, False ]]
    tPiece = [[ False,  True, False ],[  True,  True,  True ]]
    zPiece = [[  True,  True, False ],[ False,  True,  True ]]
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ "red", "yellow", "magenta", "pink",
                              "cyan", "green", "orange" ]
    newFallingPiece(app)
    app.gameOver = False

#generates a random new falling piece
def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    app.fallingPieceRow = 0
    app.numFallingPieceCols =  len(app.fallingPiece[0])
    app.fallingPieceCol = app.cols//2-app.numFallingPieceCols//2

#timer reliant actions in Tetris game app
def timerFired(app):
    if(app.gameOver==False):
        if(moveFallingPiece(app,1,0)==False):
            placeFallingPiece(app)
            if(fallingPieceIsLegal(app)==False):
                app.gameOver = True

#controller for Tetris game app
def keyPressed(app,event):
    if(app.gameOver==False):
        if(event.key=='Up'):
            rotateFallingPiece(app)
        if(event.key=='Right'):
            moveFallingPiece(app,0,1)
        if(event.key=='Left'):
            moveFallingPiece(app,0,-1)
        if(event.key=='Down'):
            hardDrop(app)
    if(event.key=='r'):
        appStarted(app)

#hard drop in response to down key
def hardDrop(app):
    while(True):
        if(moveFallingPiece(app,1,0)==False):
            break
    placeFallingPiece(app)

#controls falling piece movement
def moveFallingPiece(app,drow,dcol):
    app.fallingPieceRow+=drow
    app.fallingPieceCol+=dcol
    if(fallingPieceIsLegal(app)==False):
        app.fallingPieceRow-=drow
        app.fallingPieceCol-=dcol
        return False
    return True

#controls falling piece rotation
def rotateFallingPiece(app):
    tempPiece=app.fallingPiece
    tempPieceRows=len(tempPiece)
    tempPieceCols=len(tempPiece[0])
    newPiece=[]
    newPieceRows=tempPieceCols
    newPieceCols=tempPieceRows
    tempPieceRow=app.fallingPieceRow
    tempPieceCol=app.fallingPieceCol
    app.fallingPieceRow=app.fallingPieceRow+tempPieceRows//2-newPieceRows//2
    app.fallingPieceCol=app.fallingPieceCol+tempPieceCols//2-newPieceCols//2
    for row in range(newPieceRows):
        newPiece.append([])
        for col in range(newPieceCols):
            newPiece[row].append(None)
    for row in range(tempPieceRows):
        for col in range(tempPieceCols):
            newPiece[newPieceRows-col-1][row]=tempPiece[row][col]
    app.fallingPiece=newPiece
    if(fallingPieceIsLegal(app)==False):
        app.fallingPiece=tempPiece
        app.fallingPieceRow=tempPieceRow
        app.fallingPieceCol=tempPieceCol

#checks legality of falling piece movements
def fallingPieceIsLegal(app):  
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if(app.fallingPiece[row][col]==True):
                colPos=app.cellSize*app.fallingPieceCol
                rowPos=app.cellSize*app.fallingPieceRow
                x0=app.margin+colPos+app.cellSize*col
                y0=app.margin+rowPos+app.cellSize*row
                x1=app.margin+colPos+app.cellSize*(col+1)
                y1=app.margin+rowPos+app.cellSize*(row+1)
                if(x0<app.margin or x1>app.width-app.margin or
                   y0<app.margin or y1>app.height-app.margin):
                    return False
                if(app.board[app.fallingPieceRow+row][app.fallingPieceCol+col]
                   != 'blue'):
                    return False
    return True

#places falling piece on board and calls new falling piece
def placeFallingPiece(app):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if(app.fallingPiece[row][col]==True):
                clr=app.fallingPieceColor
                app.board[app.fallingPieceRow+row][app.fallingPieceCol+col]=clr
    removeFullRows(app)
    newFallingPiece(app)

#removes full rows that appear and scores appropriately
def removeFullRows(app):
    for row in range(app.rows):
        counter=0
        for col in range(app.cols):
            if app.board[row][col] != 'blue':
                counter+=1
        if counter == app.cols:
            app.fullRows.append(row)
    app.score+=len(app.fullRows)**2
    for row in app.fullRows:
        app.board.pop(row)
        app.board.insert(0,[])
        for col in range(app.cols):
            app.board[0].append('blue')
    app.fullRows=[]

#view for Tetris game app
def redrawAll(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='orange')
    drawBoard(app,canvas)
    drawFallingPiece(app,canvas)
    drawScore(app,canvas)
    drawGameOver(app,canvas)

#draws board
def drawBoard(app,canvas):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            drawCell(app, canvas, row, col)

#draws cells on board
def drawCell(app,canvas,row,col):
    x0=app.margin+app.cellSize*col
    y0=app.margin+app.cellSize*row
    x1=app.margin+app.cellSize*(col+1)
    y1=app.margin+app.cellSize*(row+1)
    canvas.create_rectangle(x0,y0,x1,y1,fill=app.board[row][col],width=3)

#draws falling piece
def drawFallingPiece(app,canvas):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if(app.fallingPiece[row][col]==True):
                colPos=app.cellSize*app.fallingPieceCol
                rowPos=app.cellSize*app.fallingPieceRow
                x0=app.margin+colPos+app.cellSize*col
                y0=app.margin+rowPos+app.cellSize*row
                x1=app.margin+colPos+app.cellSize*(col+1)
                y1=app.margin+rowPos+app.cellSize*(row+1)
                canvas.create_rectangle(x0,y0,x1,y1,fill=app.fallingPieceColor,
                                        width=3)

#draws game over message
def drawGameOver(app,canvas):
    if(app.gameOver):
        canvas.create_rectangle(app.margin,app.height//2-app.margin,
                                app.width-app.margin,app.height//2+app.margin,
                                fill='black')
        canvas.create_text(app.width//2,app.height//2,text='GAME OVER',
                           fill='red')

#draws updated score
def drawScore(app,canvas):
    canvas.create_text(app.width//2,app.margin//2,text='Score: %d' % app.score,
                           fill='black')

#################################################
# main
#################################################

def main():
    cs112_f19_week7_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()
