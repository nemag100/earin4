import pygame
from .board import Board
from .piece import Piece
from .constants import PLAYER1, PLAYER2, GREEN, SQUARE_SIZE, VALID_MOVES_MARKER_RADIUS
from copy import deepcopy


class Game:
    def __init__(self, initial_board=None, initial_turn=None): 
        self.selected_piece = None
        self.winner = None
        self.valid_moves = {} #for a piece
        self._init(initial_board, initial_turn)
        
   
    def _init(self, initial_board, initial_turn):
        
        self.board = Board() if initial_board is None else self.copy_board(initial_board)
        self.turn = PLAYER1 if initial_board is None else deepcopy(initial_turn)
        self.all_valid_moves = self.get_all_valid_moves_of_current_player()
        #for determining win condition   
        
    
    def get_all_valid_moves_of_current_player(self):
        all_moves = self.__get_all_moves_of_current_player()
        only_jumps = {}
        for piece_coordinates, possible_moves in all_moves.items():
            for destination, jump in possible_moves.items():
                if jump:
                    only_jumps[piece_coordinates] = possible_moves
        if only_jumps:
            return only_jumps
        else:
            return all_moves    
        
    def __get_all_moves_of_current_player(self):
        #get all nonempty moves for all pieces
        all_moves = {}
        pieces = self.get_all_pieces_of_current_player()
        for piece in pieces:
            piece_moves = self.board.get_valid_moves(piece)
            if piece_moves:
                all_moves[(piece.row, piece.column)] = piece_moves        
        return all_moves    
        
    def get_all_pieces_of_current_player(self):
        pieces = []
        for piece in self.board.get_all_pieces():
            if piece.color==self.turn:
                pieces.append(piece)
        return pieces
    
    def get_all_valid_moves_of_piece(self, piece):
        valid_moves = self.get_all_valid_moves_of_current_player().get((piece.row, piece.column))
        print(valid_moves)
        if valid_moves != None:
            return valid_moves
        else:
            return {}
         
    def copy_board(self, board_to_copy):
        self.board = deepcopy(board_to_copy)
    
    
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
            self.valid_moves = self.get_all_valid_moves_of_piece(piece)
            print("all valid moves:", self.valid_moves)
            
            return True
        return False 

    def _is_valid_move(self, row, column):
        if (row, column) in self.valid_moves:
            return True
        else:
            return False
        
    def move_piece(self, row, column):
        if self._is_valid_move(row, column):
            self.board.move_piece(self.selected_piece, row, column)
            for piece in self.valid_moves[(row,column)]: #this dictionary entry contains the pieces to be removed
                self.__remove_piece(piece)    
            
            self.change_turn()
            self.valid_moves = {}
            
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == PLAYER1:
            self.turn = PLAYER2
            enemy = "PLAYER1"
        else:
            self.turn = PLAYER1
            enemy = "PLAYER2"
        #at the beginning of turn check lose condition: I have 0 pieces or I can't move:
        self.all_valid_moves = self.get_all_valid_moves_of_current_player()
        print("Turn Changed", self.all_valid_moves)
        if not self.all_valid_moves or self.__winner():#no moves remaining
            self.winner = enemy
        
    def set_turn(self, player):
        self.valid_moves = {}
        self.all_valid_moves = self.get_all_valid_moves_of_current_player()
        self.turn = player
    
    def __remove_piece(self, piece):
        self.board.remove_piece(*piece)
    

        
    def __winner(self):
        winner = self.board.winner()
        if winner != None:
            return winner
        else:
            return False
            
    def win_message(self):
        print("WINNER IS: ", self.winner)
        self.change_turn()
        for piece in self.get_all_pieces_of_current_player():
            piece.king = True
        print("Waiting for exit.")   
        
                      
    