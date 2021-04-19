import pygame
from .board import Board
from .constants import WHITE, BLACK

class Game:
    def __init__(self, window):
       self.reset()
       self.window = window
       

    def update(self):
        self.board.draw_squares_and_pieces(self.window)
        pygame.display.update()
    
    def reset(self):
        self.selected_piece = None 
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}

    def select_piece(self, row, column):
        '''Tries to select piece for current player,
            (making sure player selects only a piece of his color)
            Tries to move the selected piece to (row column
            Updates valid_moves for the selected piece
        '''
        if self.selected_piece:
            result = self.move_piece(row, column)
            if not result: #piece not moved, reselect it
                self.selected_piece = None
                self.select_piece(row, column)
        else:
            piece = self.board.get_piece(row, column)
            if piece != 0 and piece.color == self.turn: #selected piece of my color
                self.selected_piece = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True
        return False
        
    def _move_piece(self, row, column):
        piece = self.board.get_piece(row, column)
        if self.selected_piece and piece == 0 and (row, column) in self.valid_moves:
            self.board.move_piece(self.selected_piece, row, column)   
            self.change_turn()
        else:
            return False
        return True    
    
    def change_turn(self):
        if self.turn == BLACK:
            self.turn = WHITE
        else: self.turn = BLACK
            
    
    