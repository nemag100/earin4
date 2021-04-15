import pygame
from .constants import BLACK, ROWS, COLUMNS, SQUARE_SIZE, WHITE

class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.black_pcs_left = self.white_pcs_left = 12
        self.white_kings = self.black_kings = 0
        
    def draw_squares(self, window):
        '''Draws the board pattern: alternating black and white squares in window'''
        window.fill(BLACK)
        for row in range(ROWS):
            for column in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, WHITE, (row*SQUARE_SIZE, column*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                
                
                
                
                
                
                
                
                
                
                
                