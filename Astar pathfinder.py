from pygame import *
import pygame
WIDTH =800
win = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* PathFinding Algorithm")


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Cube:
    def __init__(self, row, col, width, total_rows):
        self.row =row
        self.col =col
        self.width =width
        self.total_rows =total_rows
        self.x = row* width
        self.y = col*width
        self.color=WHITE
        self.neighbour =[]

    def getPos(self):
        return (self.x,self.y)
    
    def isClosed(self):
        return self.color ==RED
    
    def isOpen(self):
        return self.color ==GREEN
    
    def isStart(self):
        return self.color ==ORANGE
    
    def isEnd(self):
        return self.color == PURPLE
    
    def isWall(self):
        return self.color ==BLACK
    
    def reset(self):
        self.color =WHITE
    
    def setClosed(self):
        self.color=RED
    
    def setOpen(self):
        self.color=GREEN
    
    def setWall(self):
        self.color=BLACK
    
    def setEnd(self):
        self.color=PURPLE
    
    def setStart(self):
        self.color=ORANGE

    def draw(self ,win):
        pygame.draw.rect(win, self.color,(self.x,self.y,self.width,self.width))
    
    def __lt__(self, value):
        pass

def h(p1, p2):
    x1,y1 =p1
    x2,y2 =p2
    return abs(x1-x2) +abs(y1-y2)

def setGrid(rows, width):
    grid= []
    gap =width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cube = Cube(i,j,gap,rows)
            grid[i].append(cube)
    return grid

def drawGrid(win, rows , width):
    gap =width //rows
    win.fill(WHITE)
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
        pygame.draw.line(win,GREY,(i*gap,0),(i*gap,width))

def draw(win, grid,rows , width):
    win.fill(WHITE)

    for row in grid:
        for cub in row:
            cub.draw(win)
    
    drawGrid(win, rows, width)
    pygame.display.update()