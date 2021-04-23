import pygame
from .constants import WIDTH, HEIGHT, PLAYER1, PLAYER2, FPS
from .display import Display
from .game import Game
from .minmax import Minmax

class Play():
    def __init__(self):
        self.WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('EARIN Checkers @by: Szwed, Zdanowski')
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.display = Display(self.WINDOW, self.game)
        
        self.ai_player2 = None
    
    def vs_human(self):
        while self.game.winner == None:
            self.clock.tick(FPS)
            self.human_move()           
            self.display.update()
        self.play_ended()
            
    def human_move(self):
        '''catch mouse input: either a valid piece move or quit'''
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
        '''display winner message and wait for quitting'''
        self.game.win_message()
        self.display.update() #to see all pieces crowned
        while True:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
     
    def vs_ai(self, ai_PLAYER_color, depth=4):
        self.ai_player1_color = ai_PLAYER_color
        self.ai = Minmax(self.ai_player1_color, depth)
        self.display.update()

        while self.game.winner == None:
            self.clock.tick(FPS)
            self.ai_move(self.ai)
            self.human_move()  
            self.display.update()            
            
        self.play_ended()

    def ai_vs_ai(self, PLAYER1_depth=4, PLAYER2_depth=4):
        self.ai_player1_color = PLAYER1
        self.ai_player2_color = PLAYER2
        self.ai_player1 = Minmax(self.ai_player1_color, PLAYER1_depth)
        self.ai_player2 = Minmax(self.ai_player2_color, PLAYER2_depth)

        while self.game.winner == None:
            self.clock.tick(FPS)
            self.ai_move(self.ai_player1)
            self.ai_move(self.ai_player2)  
            self.display.update()            
            
        self.play_ended()

            
    def ai_move(self, ai_player):
        if  self.game.turn == ai_player.ai_color:
                self.game.board = ai_player.board_after_ai_move(self.game)
                self.game.change_turn()