from .constants import SQUARE_SIZE, PADDING, BORDER_THICKNESS, GOLD, PLAYER1, PLAYER1_BORDER_COLOR, PLAYER2_BORDER_COLOR, ALL_KINGS
import pygame
import math

class Piece:
    '''Class to store the single piece (pawn or king).
        row, column - coordinates of the piece on board
        color - color of the piece'''
    def __init__(self, row=0, column=0, color=0):
        self.row = row
        self.column = column
        self.color = color
        self.king = ALL_KINGS
        self.simulated_king = False
        self.player = None
        self.set_player()
        #white is moving up = direction is negative
        #black is moving down = direction is positives

        self.x = 0
        self.y = 0
        self._calculate_drawing_position()

        self.direction = 0
        self._set_direction()

    def set_player(self):
        '''Assigns player color to the piece.'''
        if self.color == PLAYER1:
            self.player = "P1"
        else:
            self.player = "P2"


    def _calculate_drawing_position(self):
        '''Finds the middle of the square that the piece is in.'''
        self.x = SQUARE_SIZE * self.column + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def _set_direction(self):
        '''Sets the row-wise direction in which this piece should move.'''
        if self.color == PLAYER1:
            self.direction = 1
        else:
            self.direction = -1

    def draw(self, window):
        '''Draws the piece as a circle around its x and y coordinates.'''
        radius = SQUARE_SIZE // 2 - PADDING
        border_color = ""

        if self.color == PLAYER1:
            border_color = PLAYER1_BORDER_COLOR
        else:
            border_color = PLAYER2_BORDER_COLOR

        pygame.draw.circle(window, border_color, (self.x, self.y), radius + BORDER_THICKNESS)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        if self.king:
           pygame.draw.circle(window, GOLD, (self.x, self.y), radius // 2)


    def move(self, row, column):
        '''Moves the piece into the position specified by row and column arguments.'''
        self.row = row
        self.column = column
        self._calculate_drawing_position()

    def is_king(self):
        '''Evaluates to True if the piece is king, else False.'''
        return self.king

    def set_king(self):
        '''Sets this piece to be a king.'''
        self.king = True

    def cartesian(self, other):
        '''Returns cartesian distance from this piece to the other, specified in an argument.'''
        return math.sqrt((other.row - self.row) ** 2 + (other.column - self.column) ** 2)

    def __repr__(self):
        '''Object representation, return the strings color (for debugging).'''
        return str(self.player)

