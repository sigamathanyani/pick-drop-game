import pygame
from settings import *
import random

def stageFile(filename):
    try:
        with open(filename,'r') as fileOpened:
            return fileOpened.read()
    except FileNotFoundError:
        return "File Not Found"

int_stage = int(stageFile('stage.txt'))

NUMBER_OF_TUBES = int_stage

X_MARGIN = (WIDTH - (NUMBER_OF_TUBES*TUBE_WIDTH)-((TUBE_GAP-1)*NUMBER_OF_TUBES))//2
X_MARGIN = X_MARGIN+(X_MARGIN//2)-25

class Tube:
    def __init__(self):
        self.width = TUBE_WIDTH
        self.height = TUBE_HEIGHT

    def draw(self,win,xTube,yTube=85):
        #left line
        pygame.draw.line(win,TUBE_COLOR,(xTube,yTube),(xTube,self.height),TUBE_LINE_WIDTH)
        #bottom line
        pygame.draw.line(win,TUBE_COLOR,(xTube,self.height),(xTube+self.width,self.height),TUBE_LINE_WIDTH)
        #right line
        pygame.draw.line(win,TUBE_COLOR,(xTube+self.width,yTube),(xTube+self.width,self.height),TUBE_LINE_WIDTH)

class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS

    def draw_ball(self,win,x,y,color):
        pygame.draw.circle(win,color,(x+self.radius+7,y),self.radius)

    def get_colors(self,colors): #colors is a Tuple
        picked_colors = []
        col = 0

        while col < (NUMBER_OF_TUBES-2):
            picked_color = random.randint(0,len(colors)-1)
            
            if colors[picked_color] not in picked_colors:
                picked_colors.append(colors[picked_color])
                col += 1
        return picked_colors

class Board:

    stack = []
    def __init__(self):
        pass

    def isEmpty(self,index):
        if not len(self.stack[index]):
            return True
        return False

    def isFull(self,index):
        if len(self.stack[index]) >= NUMBER_OF_BALLS:
            return True
        return False

    def poppin_item(self,index):
        if not self.isEmpty(index) and (self.isFull(index) or not self.isFull(index)):
            self.stack[index].pop()

    def adding_item(self,item,index):
        if not self.isFull(index):
            self.stack[index].append(item)
        return self.stack

def init_stack(color,stacks): # color, Array of NUMBER_OF_TUBES-2 colors.
    new_colors = color*NUMBER_OF_BALLS
    num = 0
    index = 0
    random.shuffle(new_colors)

    while num < (NUMBER_OF_TUBES-2):
        stack = []
        for i in range(NUMBER_OF_BALLS):
            stack.append(new_colors[index])
            index += 1
        stacks.append(stack)
        num += 1
    stacks.append([])
    stacks.append([])
    return stacks

def won(board_stack,win): # board_stack -> board.stack
    fontObj =pygame.font.Font('freesansbold.ttf',32)
    
    for tube in range(len(board_stack)):
        counter = 0
        
        if len(board_stack[tube]) == 0: continue
        while counter < len(board_stack[tube]):
            
            topBall = board_stack[tube][-1]
            ballPointer = board_stack[tube][counter]
            
            if topBall != ballPointer or len(board_stack[tube]) != NUMBER_OF_BALLS:
                return False
            
            counter +=1
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
                
    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        win.fill(color1)
        
        won = fontObj.render("Congradulations You Have Won",True,WHITE,NAVYBLUE)
        wonRect = won.get_rect()
        wonRect.center = (520,220)
        pygame.time.wait(300)
        pygame.display.update()
        
    return True
