import pygame
from .constants import BLACK, GRAY, ROWS, COLUMNS, SQUARE_SIZE, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        
        #board is a list of 8 rows
        #row is a list of pieces that are currently in it
        #the number 0 represents empty sqare (no pieces)
        self.board = []
        self.initialize_pieces()
        
        self.black_pcs_left = self.white_pcs_left = 12
        self.white_kings = self.black_kings = 0
        
    def draw_squares(self, window):
        '''Draws the board pattern: alternating black and white squares in window'''
        window.fill(GRAY)
        for row in range(ROWS):
            for column in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, BLACK, (row*SQUARE_SIZE, column*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def initialize_pieces(self):
        '''store initial position of pieces'''
        for row in range(ROWS):
            self.board.append([])
            for column in range(COLUMNS):
                if column % 2 == ((row + 1) % 2): #draw differently on even and odd columns
                    if row < 3: 
                        self.board[row].append(Piece(row,column,WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row,column,BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
                    
    def draw_squares_and_pieces(self, window):
        '''draw squares and stored pieces'''
        self.draw_squares(window)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw(window)
                                
    def move_piece(self, piece, row, column):
        '''Delete a piece and create it in new position'''
        #pythonic clever swap
        self.board[piece.row][piece.column], self.board[row][column]  = self.board[row][column], self.board[piece.row][piece.column]
        piece.move(row,column)
                      
        if row == ROWS or row == 0:
            if piece.king == False:
                piece.become_king()
                if piece.color == WHITE:
                    self.white_kings += 1
                else:
                    self.red_kings += 1        
                    
    def get_piece(self,row,col):
        return self.board[row][col]
    
    def get_valid_moves():
        pass
        
        
        
        
        
        
        
        
        
        
                    
                
                
                
                
                
                
                
                
                
                
                
                