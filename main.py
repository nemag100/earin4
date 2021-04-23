import pygame
from pygame.constants import WINDOWENTER
from checkers.constants import FPS, WIDTH, HEIGHT, SQUARE_SIZE, PLAYER1, PLAYER2
from checkers.board import Board
from checkers.game import Game
from checkers.display import Display
from checkers.minmax import Minmax

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('EARIN Checkers @by: Szwed, Zdanowski')

def get_mouse_row_column(mouse_pos):
    x, y = mouse_pos
    row = y // SQUARE_SIZE
    column = x // SQUARE_SIZE
    return row, column


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




def play_vs_human():
    clock = pygame.time.Clock()
    game = Game()
    display = Display(WINDOW, game)

    #setup_board_test4(game)
    while game.winner == None:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col  = get_mouse_row_column(mouse_pos)
                game.select_piece(row, col)
               
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col  = get_mouse_row_column(mouse_pos)
                
                game.move_piece(row, col)
        display.update()            
        
    game.win_message()
    display.update() 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
         #execution ended, winner is determined, wait for clicking x
         
def play_vs_ai():
    ai_player = PLAYER2
    clock = pygame.time.Clock()
    game = Game()
    display = Display(WINDOW, game)
    ai = Minmax(ai_player, depth=4)
    display.update()


    #setup_board_test4(game)
    while game.winner == None:
        clock.tick(FPS)

        if  game.turn == ai_player:
            game.board = ai.board_after_ai_move(game)
            game.change_turn()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col  = get_mouse_row_column(mouse_pos)
                game.select_piece(row, col)
               
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col  = get_mouse_row_column(mouse_pos)
                
                game.move_piece(row, col)
        display.update()            
        
    game.win_message()
    display.update() 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
         #execution ended, winner is determined, wait for clicking x
    
def main():
    play_vs_ai()

main()