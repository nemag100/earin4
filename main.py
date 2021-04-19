import pygame
from checkers.constants import FPS, WIDTH, HEIGHT, SQUARE_SIZE
from checkers.board import Board
from checkers.game import Game

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('EARIN Checkers @by: Szwed, Zdanowski')

def get_mouse_row_column(mouse_pos):
    x, y = mouse_pos
    row = y // SQUARE_SIZE
    column = x // SQUARE_SIZE
    return row, column


def main():
    running = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    
    
    while running:
        clock.tick(FPS)
        game.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, column = get_mouse_row_column(mouse_pos)

                
            
    pygame.quit()
    
main()