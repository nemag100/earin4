import pygame
from .board import Board
from .piece import Piece
from .constants import PLAYER1, PLAYER2, GREEN, SQUARE_SIZE, VALID_MOVES_MARKER_RADIUS

class Game:
    def __init__(self, window):
        self.window = window    
        self._init()
            

    def update(self):
        self.board.draw_board(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    
    def _init(self):
        self.selected_piece = None
        self.board = Board()
        self.turn = PLAYER1
        self.valid_moves = {} #for a piece
        self.all_valid_moves = {}

    def reset(self): #resetting is the same as initializing once again
        self._init()
    
    def select_piece(self, row, column):
        '''Tries to select piece for current player,
            (making sure player selects only a piece of his color)
            Tries to move the selected piece to (row column
            Updates valid_moves for the selected piece
        '''
        piece = self.board.get_piece(row, column)
        if piece != 0 and piece.color == self.turn: #selected piece of my color
            self.selected_piece = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False
            
      #  if self.selected_piece:
      ##      result = self._move_piece(row, column)
       #     if not result: #piece not moved, reselect it
      #          self.selected_piece = None
     #           self.select_piece(row, column)
        
    def _is_valid_move(self, row, column):
        if (row, column) in self.valid_moves:
            return True
        else:
            return False
        
    def move_piece(self, row, column):
        if self._is_valid_move(row, column):
            self.board.move_piece(self.selected_piece, row, column)
            for piece in self.valid_moves[(row,column)]: #this dictionary entry contains the pieces to be removed
                self.remove_piece(piece)
            self.change_turn()
            self.valid_moves = {}
            
    
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == PLAYER1:
            self.turn = PLAYER2
        else:
            self.turn = PLAYER1
    
    def set_turn(self, player):
        self.valid_moves = {}
        self.turn = player
    
    def remove_piece(self, piece):
        self.board.remove_piece(*piece)
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, column = move
            pygame.draw.circle(self.window, GREEN, (column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), VALID_MOVES_MARKER_RADIUS)
        
    def winner(self):
        return self.board.winner()  
            
        
        
                      
    