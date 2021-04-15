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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            
        board.draw_squares(WINDOW)
        pygame.display.update()
    pygame.quit()
    
main()