from .game import Game
import pygame
from .constants import GREEN, SQUARE_SIZE, VALID_MOVES_MARKER_RADIUS

class Display:
    '''Class for controlling the display.'''
    def __init__(self, window, game):
        self.window = window
        self.game = game

    def update(self):
        '''Updates the display with the current state of the board.'''
        self.game.board.draw_board(self.window)
        self.draw_valid_moves(self.game.valid_moves)
        pygame.display.update()

    def draw_valid_moves(self, moves):
        '''Draws hints for valid moves for the selected piece.'''
        for move in moves:
            row, column = move
            pygame.draw.circle(self.window, GREEN, (column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), VALID_MOVES_MARKER_RADIUS)

    def get_mouse_row_column(self, mouse_pos):
        '''Returns mouse position by means of row and column of the board.'''
        x, y = mouse_pos
        row = y // SQUARE_SIZE
        column = x // SQUARE_SIZE
        return row, column
