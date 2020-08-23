import pygame
import math
from queue import PriorityQueue
import tkinter as tk
from tkinter.messagebox import *


VISUALIZE  =True
WIDTH =700       # Change to reduse or increse the size of Window
ROWS =25         # Change This to Change The Number of block(s) in grid Recomended size -25 50 100
win = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* PathFinding Algorithm")


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)


class Cube:
    def __init__(self, row, col, width, total_rows):
        self.row =row
        self.col =col
        self.width =width
        self.total_rows =total_rows
        self.x = row* width
        self.y = col*width
        self.color=WHITE
        self.neighbours =[]

    def getPos(self):
        return self.row,self.col
    
    def isClosed(self):
        return self.color ==RED
    
    def isOpen(self):
        return self.color ==GREEN
    
    def isStart(self):
        return self.color ==ORANGE
    
    def isEnd(self):
        return self.color == PURPLE
    
    def isWall(self):
        return self.color == BLACK
    
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
    def setPath(self):
        self.color=BLUE

    def draw(self ,win):
        pygame.draw.rect(win, self.color,(self.x,self.y,self.width,self.width))

    def updateNeighbour(self,grid):
        self.neighbours =[]
        if self.row<self.total_rows-1 and not grid[self.row+1][self.col].isWall():
            self.neighbours.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].isWall():
            self.neighbours.append(grid[self.row-1][self.col])

        if self.col<self.total_rows-1 and not grid[self.row][self.col+1].isWall():
            self.neighbours.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].isWall():
            self.neighbours.append(grid[self.row][self.col-1])

    
    def __lt__(self, value):
        return False

def h(p1, p2):
    x1,y1 =p1
    x2,y2 =p2
    return abs(x1-x2) +abs(y1-y2)

def reconstructPath(camefrom, end, draw):
    current =end
    while current in camefrom:
        current = camefrom[current]
        current.setPath()
        if VISUALIZE:
            draw()


def algorithm(draw, grid, start, end):
    count =0
    openSet= PriorityQueue()
    openSet.put((0, count, start))
    openSetHash={start}
    cameFrom ={}
    g_score={cube:float("inf") for rows in grid for cube in rows}
    f_score={cube:float("inf") for rows in grid for cube in rows}
    g_score[start]=0
    f_score[start]= h(start.getPos(),end.getPos())

    while not openSet.empty():
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        
        current  = openSet.get()[2]
        openSetHash.remove(current)
        if current == end:
            end.setEnd()
            reconstructPath(cameFrom, end , draw)
            start.setStart()
            return True
        
        for neighbour in current.neighbours:
            tempGscore = g_score[current]+1

            if tempGscore <g_score[neighbour]:
                cameFrom[neighbour]= current
                g_score[neighbour] =tempGscore
                f_score[neighbour] = tempGscore +h(neighbour.getPos(),end.getPos())
                if neighbour not in openSetHash:
                    count+=1
                    openSet.put((f_score[neighbour], count, neighbour))
                    openSetHash.add(neighbour)
                    if VISUALIZE:
                        neighbour.setOpen()     
        
        if VISUALIZE:
            draw()

        if current != start and VISUALIZE:
            current.setClosed()

    return False

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

def getClickedPos(pos, rows, width):
    x, y =pos
    gap =width//rows
    rows = x//gap
    col =  y//gap
    return rows,col

def main(win, width,ROWS):
    grid = setGrid(ROWS, width)


    run = True
    started = False

    start = None
    end = None

    while run :
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started:
                continue
            
            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row , col = getClickedPos(pos,ROWS , width)
                cube= grid[row][col]
                if not start and cube!=end:
                    start=cube
                    cube.setStart()
                    cube.draw(win)
                elif not end and cube !=start:
                    end = cube
                    cube.setEnd()
                    cube.draw(win)
                elif cube != end and cube != start:
                    cube.setWall()
                    cube.draw(win)
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row , col = getClickedPos(pos,ROWS , width)
                cube= grid[row][col]
                if cube == start :
                    start = None
                elif cube ==end:
                    end =None 
                cube.reset()
                cube.draw(win)
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_SPACE and start and end:
                    for row in grid:
                        for cube in row:
                            cube.updateNeighbour(grid)
                    algorithm(lambda: draw(win,grid,ROWS,width), grid ,start ,end)
                if event.key ==pygame.K_c:
                    start =None
                    end   =None
                    grid = setGrid(ROWS, width)

                

root = tk.Tk()
root.withdraw()

msg =tk.messagebox.askquestion ('Selection','Do You Want To Visualize The Algorithm ?\n\nYes- See How the Algorith Works with Visualization\nNo- Faster with out Visualization',icon = 'question') 
if (True):  # change this to False if u dont want instructions
        tk.messagebox.showinfo("Key List","PRESS\nLEFT CLICK    - To place START/END point and Draw walls\nRIGHT CLICK - Remove START/END and walls \nSPACE\t      - Start The algorithm\nC\t      - To Clear Screen ")
if msg  =="yes":
    VISUALIZE =True
else:
    VISUALIZE =False
main(win, WIDTH, ROWS)