import pygame
from checkers.constants import FPS, WIDTH, HEIGHT
from checkers.board import Board

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('EARIN Checkers @by: Szwed, Zdanowski')

def main():
    running = True
    clock = pygame.time.Clock()
    
    while running:
        clock.tick(FPS)
        board = Board()
        board.draw_squares_and_pieces(WINDOW)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            
    pygame.quit()
    
main()