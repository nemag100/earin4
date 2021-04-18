from .constants import BLACK, SQUARE_SIZE, WHITE, PADDING, BORDER_THICKNESS, GOLD
import pygame

class Piece:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.king = False
        #white is moving up = direction is negative
        #black is moving down = direction is positive
        if self.color == WHITE:
            self.direction = -1
        else:
            self.direction = 1   
        
        self.x = 0
        self.y = 0   
        self.calculate_position()

    def calculate_position(self):
        '''Finds the middle of the square that the piece is in.'''
        self.x = SQUARE_SIZE * self.column + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
        
    def become_king(self):
        self.king == True
        
        
    def draw(self, window):
        '''Draws the piece as a circle around its x and y'''
        radius = SQUARE_SIZE // 2 - PADDING
        border_color = ""
        
        if self.color == WHITE:
            border_color = BLACK
        else:
            border_color = WHITE
            
        pygame.draw.circle(window, border_color, (self.x, self.y), radius + BORDER_THICKNESS)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        if self.king:
           pygame.draw.circle(window, GOLD, (self.x, self.y), radius // 2)
        
        
    def __repr__(self):
        '''object representation, return the strings color (for debugging)'''
        return str(self.color)
        
    def move(self, row, column):
        self.row = row
        self.column = column
        self.calculate_position()
            
            