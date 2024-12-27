import pygame
import sys
import random, pygame, sys
from pygame.locals import *

# Initialize constants
FPS = 30
WINDOWWIDTH = 500
WINDOWHEIGHT = 500
BOXSIZE = 80
GAPSIZE = 10
BOARDWIDTH = 5
BOARDHEIGHT = 5
assert BOARDWIDTH * BOARDHEIGHT == 25, "Board should be 5x5."

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLORS = [RED, GREEN, BLUE, YELLOW]

# Calculate margins to center the board
XMARGIN = (WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) // 2
YMARGIN = (WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) // 2

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Color Fill Puzzle')

    board = [[None for _ in range(BOARDHEIGHT)] for _ in range(BOARDWIDTH)]

    while True:
        mouseClicked = False

        DISPLAYSURF.fill(WHITE)
        drawBoard(board)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                boxx, boxy = getBoxAtPixel(mousex, mousey)
                if boxx is not None and boxy is not None:
                    mouseClicked = True

        if mouseClicked:
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            if board[boxx][boxy] is None:
                board[boxx][boxy] = 0
            else:
                board[boxx][boxy] = (board[boxx][boxy] + 1) % len(COLORS)

            if not isValidMove(board, boxx, boxy):
                board[boxx][boxy] = (board[boxx][boxy] - 1) % len(COLORS)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawBoard(board):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if board[boxx][boxy] is not None:
                color = COLORS[board[boxx][boxy]]
                pygame.draw.rect(DISPLAYSURF, color, (left, top, BOXSIZE, BOXSIZE))
            pygame.draw.rect(DISPLAYSURF, BLACK, (left, top, BOXSIZE, BOXSIZE), 1)

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def isValidMove(board, boxx, boxy):
    color = board[boxx][boxy]
    adjacentBoxes = [(boxx - 1, boxy), (boxx + 1, boxy), (boxx, boxy - 1), (boxx, boxy + 1)]
    for adjx, adjy in adjacentBoxes:
        if 0 <= adjx < BOARDWIDTH and 0 <= adjy < BOARDHEIGHT:
            if board[adjx][adjy] == color:
                return False
    return True

if __name__ == "__main__":
    main()
