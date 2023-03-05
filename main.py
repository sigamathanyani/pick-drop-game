import pygame, sys
from pygame.locals import *
from settings import *
from plays import Tube, Ball, Board
from plays import init_stack, stageFile, won
import random

int_stage = int(stageFile('stage.txt'))

NUMBER_OF_TUBES = int_stage

X_MARGIN = (WIDTH - (NUMBER_OF_TUBES*TUBE_WIDTH)-((TUBE_GAP-1)*NUMBER_OF_TUBES))//2
X_MARGIN = X_MARGIN+(X_MARGIN//2)-25

assert NUMBER_OF_TUBES >= 5, "Number of tubes should be greater than 5"
assert NUMBER_OF_TUBES % 2 != 0, "Number of tubes should be odd"

pygame.init()
fpsClock = pygame.time.Clock()

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("pick and drop")

fontObj =pygame.font.Font('freesansbold.ttf',32)

y_offset = 35

def main():
    tubes = Tube()
    balls = Ball()
    board = Board()
    pickedColors = balls.get_colors(ALLCOLORS)
    hold = False
    heldTube = None
    first_tube, second_tube = None, None
    undo_turns,redo_turns = True, False
    
    pickedColor = init_stack(pickedColors,board.stack)
    #print(board.stack)
    isWon = won(board.stack,win)

    while True:
        win.fill(BGCOLOR)

        for tube in range(len(board.stack)):
            tubes.draw(win,(tube*(TUBE_WIDTH+TUBE_GAP))+X_MARGIN)
            
            for ball in range(len(board.stack[tube])):

                balls.draw_ball(win,
                                (tube*(TUBE_WIDTH+TUBE_GAP))+X_MARGIN,
                                215-y_offset*ball,
                               pickedColor[tube][ball])
                
                pygame.Rect(tube*(TUBE_WIDTH+TUBE_GAP)+X_MARGIN,
                85,
                TUBE_WIDTH,
                TUBE_HEIGHT)

        for event in pygame.event.get():
            isWon = won(board.stack,win)
            if isWon:
                board.stack = []
                pickedColors = balls.get_colors(ALLCOLORS)
                pickedColor = init_stack(pickedColors,board.stack)
                NUMBER_OF_TUBES = 7
                
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
  
                for tube in range(len(board.stack)):
                    tube_rect = pygame.Rect(tube*(TUBE_WIDTH+TUBE_GAP)+X_MARGIN,
                                0,
                                TUBE_WIDTH,
                                TUBE_HEIGHT)
                
                    if tube_rect.collidepoint(mouse_pos):
                        if hold:
                            if board.isEmpty(tube) or heldCol == board.stack[tube][-1]:
                                if not board.isFull(tube):
                                    board.adding_item(heldCol,tube)
                                    
                                else: board.adding_item(heldCol,heldTube)
                            else: board.adding_item(heldCol,heldTube)
                            hold = not hold
                            turns = True
                                
                        elif not hold and not board.isEmpty(tube):
                            heldCol = board.stack[tube][-1]
                            board.poppin_item(tube)
                            heldTube = tube
                            hold = not hold

                        second_tube = first_tube
                        first_tube = tube
                        
                if restartRect.collidepoint(mouse_pos):
                    for tube in range(len(board.stack)):
                        for ball in range(len(board.stack[tube])):
                            board.stack = []
                            pickedColors = balls.get_colors(ALLCOLORS)
                            pickedColor = init_stack(pickedColors,board.stack)  
                            
                if redoRect.collidepoint(mouse_pos) and not hold and redo_turns:
                    board.adding_item(heldCol,first_tube)
                    board.poppin_item(second_tube)
                    redo_turns = False
                    undo_turns = True
                    
                if undoRect.collidepoint(mouse_pos) and not hold and undo_turns:
                    board.adding_item(heldCol,second_tube)
                    board.poppin_item(first_tube)
                    undo_turns = False
                    redo_turns = True
                            
        if hold:
            mouse_pos = event.pos
            balls.draw_ball(win,mouse_pos[0]-21,mouse_pos[1],heldCol)

        restart = fontObj.render("Restart",True,WHITE,NAVYBLUE)
        restartRect = restart.get_rect()
        restartRect.center = (520,350)

        undo = fontObj.render("Undo",True,WHITE,NAVYBLUE)
        undoRect = undo.get_rect()
        undoRect.center = (250,350)

        redo = fontObj.render("Redo",True,WHITE,NAVYBLUE)
        redoRect = restart.get_rect()
        redoRect.center = (750,350)

        win.blit(restart,restartRect)
        win.blit(redo,redoRect)
        win.blit(undo,undoRect)

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()

