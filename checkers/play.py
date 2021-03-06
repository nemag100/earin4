import sys
import pygame
from .constants import WIDTH, HEIGHT, PLAYER1, PLAYER2, FPS, CLASSIC, SQUARED_PAWNS, EXPANSIVE, END_GAME
from .display import Display
from .game import Game
from .minmax import Minmax
from time import sleep

class Play():
    '''
    Class for controlling the clock and display and serving different modes of games.
    '''
    def __init__(self):
        self.WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('EARIN Checkers @by: Szwed, Zdanowski')
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.display = Display(self.WINDOW, self.game)
        self.ai_player2 = None

    def vs_human(self):
        '''Method for the player vs. player game mode.'''
        while self.game.winner == None:
            self.clock.tick(FPS)
            self.human_move()
            self.display.update()
        self.play_ended()

    def human_move(self):
        '''Catches mouse input: either a valid piece move or quit.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col  = self.display.get_mouse_row_column(mouse_pos)
                self.game.select_piece(row, col)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col  = self.display.get_mouse_row_column(mouse_pos)
                self.game.move_piece(row, col)

    def play_ended(self):
        '''Displays winner message and wait for quitting.'''
        self.game.win_message()
        self.display.update() #to see all pieces crowned
        while True:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

    def vs_ai(self, ai_PLAYER_color, depth=4, ai_heuristic=CLASSIC, adaptive_heuristics=False):
        '''Method for the player vs. AI game mode.
           ai_PLAYER_color - color of AI player
           depth - depth of min-max algorithm with aplha-beta pruning used by the AI
           ai_heuristic - heuristic used by the AI
           adaptive_heuristics - if True, AI uses more advanced, adaptive heuristics'''
        self.ai = Minmax(ai_PLAYER_color, depth=depth, heuristic=ai_heuristic, adaptive_heuristics=adaptive_heuristics)
        self.display.update()

        while self.game.winner == None:
            self.clock.tick(FPS)
            if self.game.turn == ai_PLAYER_color:
                self.ai_move(self.ai)
            else:
                self.human_move()
            self.display.update()

        self.play_ended()

    def ai_vs_ai(self, PLAYER1_depth=4, PLAYER2_depth=4, PLAYER1_heuristic=CLASSIC, PLAYER2_heuristic=CLASSIC, adaptive_heuristics=False):
        '''Method for the AI vs. AI game mode.
            PLAYER1_depth - depth of min-max algorithm with aplha-beta pruning used by the AI player 1
            PLAYER2_depth - depth of min-max algorithm with aplha-beta pruning used by the AI player 2
            PLAYER1_heuristic - heuristic used by the AI player 1
            PLAYER2_heuristic - heuristic used by the AI player 2
            adaptive_heuristics - if True, AI uses more advanced, adaptive heuristics'''
        self.game.acknowledge_ava()
        self.ai_player1_color = PLAYER1
        self.ai_player2_color = PLAYER2
        self.ai_player1 = Minmax(self.ai_player1_color, depth=PLAYER1_depth, heuristic=PLAYER1_heuristic, adaptive_heuristics=adaptive_heuristics)
        self.ai_player2 = Minmax(self.ai_player2_color, depth=PLAYER2_depth, heuristic=PLAYER2_heuristic, adaptive_heuristics=adaptive_heuristics)
        self.display.update()

        while self.game.winner == None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 0
            self.clock.tick(FPS)
            if  self.game.turn == self.ai_player1_color:
                self.ai_move(self.ai_player1)
            elif self.game.turn == self.ai_player2_color:
                self.ai_move(self.ai_player2)
            self.display.update()

        self.play_ended()

    def ai_move(self, ai_player):
        '''Method for AI move.'''
        sleep(1) # to keep track of AI moves more easily
        self.piece_coords, self.move_coords = ai_player.ai_move(self.game)
        self.game.select_piece(*self.piece_coords)
        self.game.move_piece(*self.move_coords)
