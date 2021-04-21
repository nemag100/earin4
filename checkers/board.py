import pygame
from .constants import ROWS, COLUMNS, SQUARE_SIZE, PLAYER1, PLAYER2, LEFT_CORNER_SQUARE_COLOR, RIGHT_CORNER_SQUARE_COLOR
from .piece import Piece

class Board:
    def __init__(self):
        
        #board is a list of 8 rows
        #row is a list of pieces that are currently in it
        #the number 0 represents empty sqare (no piece object)
        self.board = []
        self._initial_board()
        
        self.player1_pcs_left = self.player2_pcs_left = 12
        self.player1_kings = self.player2_kings = 0
    
    def _initial_board(self):
        '''create board with initial positions'''
        for row in range(ROWS):
            self.board.append([])
            for column in range(COLUMNS):
                if column % 2 == ((row + 1) % 2): #draw differently on even and odd columns
                    if row < 3: 
                        self.board[row].append(Piece(row,column,PLAYER1))
                    elif row > 4:
                        self.board[row].append(Piece(row,column,PLAYER2))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        

    def draw_board(self, window):
        '''draw squares and stored pieces'''
        self.draw_squares(window)
        self.draw_pieces(window)    

        
    def draw_squares(self, window):
        '''Draws the board pattern: alternating black and white squares in window'''
        window.fill(LEFT_CORNER_SQUARE_COLOR)
        for row in range(ROWS):
            for column in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, RIGHT_CORNER_SQUARE_COLOR, (row*SQUARE_SIZE, column*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
   
    def draw_pieces(self, window):
        for row in range(ROWS):
            for column in range(COLUMNS):
               # piece = self.board[row][column]
                piece = self.get_piece(row,column)
                if piece != 0:
                    piece.draw(window)
    
                                
    def move_piece(self, piece, new_row, new_column):
        '''Delete a piece and create it in new position'''
        #pythonic clever swap
        self.board[piece.row][piece.column], self.board[new_row][new_column]  = self.board[new_row][new_column], self.board[piece.row][piece.column]
        piece.move(new_row,new_column)            
        
        if new_row == ROWS - 1 or new_row == 0: #moved to the edge of the board
            self.set_king(piece)       

                   
    def get_piece(self,row,column):
        if 0 <= row < ROWS and 0 <= column < COLUMNS:
            return self.board[row][column]
        else: #index out of range
            return None
        
    def set_king(self, piece):
        if piece.is_king() == False:
            piece.set_king()
            if piece.color == PLAYER1:
                self.player1_kings += 1
            else:
                self.player2_kings += 1
    
    def add_piece(self, row, column, player, king):
        ''' use for testing purposes only, adds any piece to any position,
            overwriting existing one
        '''
        if 0 <= row < ROWS and 0 <= column < COLUMNS:

            piece = self.board[row][column] = Piece(row, column, player)
            piece.king = king
            if piece.color == PLAYER1:
                if self.player1_pcs_left == None:
                    self.player1_pcs_left = 1
                    if king:
                        self.player1_kings += 1
                else:
                    self.player1_pcs_left += 1
                    if king:
                        self.player2_kings += 1
            
            if piece.color == PLAYER2:
                if self.player2_pcs_left == None:
                    self.player2_pcs_left = 1
                else:
                    self.player2_pcs_left += 1
            
            
                 
               
    def remove_all_pieces(self):
        for row in range(ROWS):
            for col in range(COLUMNS):
                self.remove_piece(row,col)
        self.player1_pcs_left = None #prevents from instantly winning
        self.player2_pcs_left = None
        self.player1_kings = 0
        self.player2_kings = 0

    
        
    def is_king(self, piece):
        return piece.is_king()
      
###############poniższe do naprawy




    
    def get_valid_moves(self, piece):
        moves = {}
        moves.update(self._get_valid_moves(piece, piece.row, piece.column, [], 2))

        if len(moves) == 0: 
            moves.update(self._get_valid_moves(piece, piece.row, piece.column, [], 1))
        else:
            
        #delete moves contained in another move 
            to_del = set() #store keys of entries to delete
            del_me = False #flag to delete currently examined key
            for key, val in moves.items(): #compare the dictionary entries
                for k, v in moves.items(): #which differ by 1 in length
                    for i in range(0, len(val)): #and shorter value is included in longer
                        if len(v) - len(val) == 1 and val[i] == v[i]:
                            del_me = True #as long as the elements are the same keep the flag as true
                        else:
                            del_me = False #unique element detected = sequences are different, compare with next one
                            break
                    if del_me:
                        to_del.add(key) #if the whole shorter sequence is included in the longer one, add the shorter's key to delete
            for key in to_del: 
                del moves[key] #remove all entries flagged to delete

        
        
        
        
        
        
           
        return moves
    
    def _get_valid_moves(self, piece, row, col, jump_path, step_size):
        ''' this method takes in a row and col of where the piece is currently during the jump. It also takes a jump_path so a king
        does not jump back to where it came from and to prevent jumping over the same piece twice.
        Finally a step_size is provided: if it's 1 only short jumps are considered, if 2 then jump chains are considered
        '''
        up, down, left, right = [x + y * step_size for x in [row, col] for y in [-1, +1]]
        moves = {}

        for new_col in [left, right]:
            for new_row in [up, down]:
                if not self.can_jump_from_to(piece, row, col, new_row, new_col, step_size):
                    continue
                
                if step_size == 1:
                    moves[new_row, new_col] = []
                else:
                    middle_row = (new_row + row) // 2
                    middle_col = (new_col + col) // 2
                    if (middle_row, middle_col) in jump_path:
                        continue
                    new_jump_path = jump_path.copy()
                    new_jump_path.append((middle_row, middle_col))
                    moves[(new_row, new_col)] = new_jump_path
                    # recursive call
                    
                    moves.update(self._get_valid_moves(piece, new_row, new_col, new_jump_path, step_size))
        return moves    
    
    def can_jump_from_to(self, piece, old_row, old_col, new_row, new_col, step_size) -> bool:
        ''' evaluates to True if boundaries are right and if current piece between start/end location is of different color'''
        if not (piece.is_king() or new_row == old_row + piece.direction * step_size):
            # invalid direction
            return False
        if not (0 <= new_row < ROWS and 0 <= new_col < COLUMNS): #is new_row inside of <0, ROWS) ? and similarly new_col
            # outside of board
            return False
        new_loc = self.get_piece(new_row, new_col)
        if new_loc != 0:
            # jump location not empty
            return False
        # all base obstacles have been overcome
        if step_size == 2:
            middle_row = (old_row + new_row) // 2
            middle_col = (old_col + new_col) // 2
            middle_piece = self.get_piece(middle_row, middle_col)
            if middle_piece == 0 or middle_piece.color == piece.color:
                return False
        
        return True
           
                
    
        
   

    def remove_piece(self, row, col):
        if (0 <= row < ROWS and 0 <= col < COLUMNS):
            piece = self.get_piece(row,col)
            
            if piece != None and piece != 0 and self.player2_pcs_left != None and piece.color == PLAYER2:
                self.player2_pcs_left -= 1
            elif self.player1_pcs_left != None:
                self.player1_pcs_left -= 1
            self.board[row][col] = 0    
                
                
    def winner(self):
        if self.player1_pcs_left != None and self.player1_pcs_left <= 0:
            return "PLAYER2"
        elif self.player2_pcs_left != None and self.player2_pcs_left <=0:
            return "PLAYER1"
        return None
                
                
                
                
                
                
                
                
                
                
                
                