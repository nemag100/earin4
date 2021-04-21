import pygame
from checkers.constants import FPS, WIDTH, HEIGHT, SQUARE_SIZE, PLAYER1, PLAYER2
from checkers.board import Board
from checkers.game import Game

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
    game.set_turn(PLAYER1)
    game.board.add_piece(2, 1, PLAYER1, king=True)
    game.board.add_piece(3, 2, PLAYER2, king=True)
    game.board.add_piece(3, 4, PLAYER2, king=True)
    game.board.add_piece(1, 4, PLAYER2, king=True)
    game.board.add_piece(3, 6, PLAYER2, king=True)
    game.board.add_piece(5, 6, PLAYER2, king=True)
    game.board.add_piece(6, 7, PLAYER1, king=True)
    
def setup_board_test3(game): #testing win condition
    game.board.remove_all_pieces()
    game.set_turn(PLAYER2)
    game.board.add_piece(2, 1, PLAYER1, king=True)
    game.board.add_piece(3, 2, PLAYER2, king=True)

def main():
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    setup_board_test2(game)
    while game.update_winner():
        clock.tick(FPS)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col  = get_mouse_row_column(mouse_pos)
                game.select_piece(row, col)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col  = get_mouse_row_column(mouse_pos)
                
                game.move_piece(row, col)
                
        
#    pygame.quit()
    game.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
         #execution ended, winner is determined, wait for clicking x
main()