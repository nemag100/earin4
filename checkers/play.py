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
    
    def vs_human(self):
        while self.game.winner == None:
            self.clock.tick(FPS)
            self.human_move_with_mouse()           
            self.display.update()
        self.play_ended()
            
    def human_move_with_mouse(self):
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
     
         
    def vs_ai(self):
        ai_player = PLAYER2
        clock = pygame.time.Clock()
        game = Game()
        display = Display(self.WINDOW, game)
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
                    row, col  = display.get_mouse_row_column(mouse_pos)
                    game.select_piece(row, col)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    row, col  = display.get_mouse_row_column(mouse_pos)
                    
                    game.move_piece(row, col)
            display.update()            
            
        game.win_message()
        display.update() 
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            #execution ended, winner is determined, wait for clicking x