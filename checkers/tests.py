from .game import Game
from .board import Board
from .constants import PLAYER1, PLAYER2

def setup_board_test1(game):
    '''Manual testing tools:
        1. Use game.board.remove_all_pieces()
        2. Use game.board.add_piece to add any pieces. remember to add only on black squares!
        3. Use game.set_turn(player) or game.change_turn()
    '''
    game.board.remove_all_pieces()
    game.set_turn(PLAYER1)
    game.board.add_piece(2, 1, PLAYER1, king=True)
    game.board.add_piece(3, 2, PLAYER2, king=True)
    game.board.add_piece(3, 4, PLAYER2, king=True)
    game.board.add_piece(1, 4, PLAYER2, king=True)
    game.board.add_piece(3, 6, PLAYER2, king=True)
    game.board.add_piece(5, 6, PLAYER2, king=True)
    
def setup_board_test2(game):
    '''Manual testing tools:
        1. Use game.board.remove_all_pieces()
        2. Use game.board.add_piece to add any pieces. remember to add only on black squares!
        3. Use game.set_turn(player) or game.change_turn()
    '''
    game.board.remove_all_pieces()
    game.board.add_piece(2, 1, PLAYER1, king=True)
    game.board.add_piece(3, 2, PLAYER2, king=True)
    game.board.add_piece(3, 4, PLAYER2, king=True)
    game.board.add_piece(1, 4, PLAYER2, king=True)
    game.board.add_piece(3, 6, PLAYER2, king=True)
    game.board.add_piece(5, 6, PLAYER2, king=True)
    game.board.add_piece(6, 7, PLAYER1, king=True)
    game.board.add_piece(6, 1, PLAYER1, king=True)
    game.get_all_valid_moves_of_current_player()
    
def setup_board_test3(game): #testing win condition
    game.board.remove_all_pieces()
    game.set_turn(PLAYER2)
    game.board.add_piece(4, 1, PLAYER1, king=False)
    game.board.add_piece(5, 2, PLAYER2, king=False)
    
def setup_board_test4(game): #testing no possible moves win condition
    game.board.remove_all_pieces()
    game.board.add_piece(0, 7, PLAYER1, king=False)
    game.board.add_piece(3, 0, PLAYER1, king=False)
    game.board.add_piece(3, 2, PLAYER1, king=False)
    game.board.add_piece(3, 4, PLAYER1, king=False)
    game.board.add_piece(3, 6, PLAYER1, king=False)
    game.board.add_piece(2, 1, PLAYER1, king=False)
    game.board.add_piece(2, 3, PLAYER1, king=False)
    game.board.add_piece(2, 5, PLAYER1, king=False)
    game.board.add_piece(2, 7, PLAYER1, king=False)
    game.board.add_piece(4, 1, PLAYER2, king=False)
    game.board.add_piece(4, 3, PLAYER2, king=False)
    game.board.add_piece(4, 5, PLAYER2, king=False)
    game.board.add_piece(4, 7, PLAYER2, king=False)
    game.board.add_piece(5, 0, PLAYER2, king=False)
    game.board.add_piece(5, 2, PLAYER2, king=False)
    game.board.add_piece(5, 4, PLAYER2, king=False)
    game.board.add_piece(5, 6, PLAYER2, king=False)
    game.board.add_piece(7, 0, PLAYER2, king=False)