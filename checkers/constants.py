import pygame
import os
#Window properties
WIDTH, HEIGHT = 800, 800

#Board properties
ROWS, COLUMNS = 8, 8
SQUARE_SIZE = WIDTH // COLUMNS

#Piece properties
PADDING = 10 #distance between piece and square
BORDER_THICKNESS = 2

#RGB colors
RED     =  (255, 0, 0)
GREEN   =  (0, 255, 0)
BLUE    =  (0, 0, 255)
BLACK   =  (0, 0, 0)
WHITE   =  (255, 255, 255)
GRAY    =  (128, 128, 128)
BUFF    =  (218, 160, 109)
GOLD    =  (255, 215, 0)

#Game properties
FPS = 60