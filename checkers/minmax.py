import math
from copy import deepcopy
import pygame
from .constants import PLAYER1, PLAYER2
from .game import Game

class Minmax:

    def __init__(self, ai_color, depth=4):
        '''depth - search depth for alpha-beta algorithm
           AI maximizes, human minimizes'''
        self.ai_color = ai_color
        self.depth = depth
        self.__set_human_color()
        self.inf   = math.inf
        self.ninf  = -math.inf

    def __set_human_color(self):
        if self.ai_color == PLAYER1:
            self.human_color = PLAYER2
        else:
            self.human_color = PLAYER1

    def get_all_moves(self, game):
        games_after_one_move = [] #list of games to return
        copied_game = deepcopy(game)

        valid_moves = copied_game.get_all_valid_moves_of_current_player()
        print("Valid moves: ", valid_moves)
        for piece_coords, piece_moves in valid_moves.items():
            for destination in piece_moves.keys():            #for every move
                copied_game = deepcopy(game)       #make a copy of current game
                copied_game.select_piece(*piece_coords) #move the piece
                copied_game.move_piece(*destination)
                                                #save the game after moving
                games_after_one_move.append(copied_game)
#debug
        print("All valid boards: ")
        for g in games_after_one_move:
            print(str(g))
#debug
        return games_after_one_move

    def alphabeta(self, game):
        if game.turn == self.human_color:
            print("human")
            _, best_move = self.min_alphabeta(game, self.depth, self.ninf, self.inf)
        elif game.turn == self.ai_color:
            print("ai")
            _, best_move = self.max_alphabeta(game, self.depth, self.ninf, self.inf)
        return best_move

    def max_alphabeta(self, game, depth, alpha, beta):
        '''Alpha-beta function for the maximizing player.
           AI maximizes'''
        if depth == 0 or game.winner != None:
            return self.evaluate(game), game.board
        max_eval = self.ninf
        best_move = None
        for game_after_one_move in self.get_all_moves(game):   
            evaluation = self.min_only_eval(game_after_one_move, depth-1, alpha, beta)
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = game_after_one_move.board
            if max_eval >= beta:
                return max_eval, best_move
            if max_eval > alpha:
                alpha = max_eval
        print("===========================================\n")
        print(best_move.board)
        return max_eval, best_move
    
    def min_alphabeta(self, game, depth, alpha, beta):
        '''Alpha-beta function for the minimizing player.
           Human minimizes'''
        if depth == 0 or game.winner != None:
            return self.evaluate(game), game.board
        min_eval = self.inf
        best_move = None
        for game_after_one_move in self.get_all_moves(game):
            evaluation = self.max_only_eval(game_after_one_move, depth-1, alpha, beta)
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = game_after_one_move.board
            if min_eval <= alpha:
                return min_eval, best_move
            if min_eval < beta:
                beta = min_eval
        return min_eval, best_move
    
    
    def max_only_eval(self, game, depth, alpha, beta):
        '''Alpha-beta function for the maximizing player.
           AI maximizes'''
        if depth == 0 or game.winner != None:
            return self.evaluate(game)
        max_eval = self.ninf
        for game_after_one_move in self.get_all_moves(game):
            evaluation = self.min_only_eval(game_after_one_move, depth-1, alpha, beta)
            if evaluation > max_eval:
                max_eval = evaluation
            if max_eval >= beta:
                return max_eval
            if max_eval > alpha:
                alpha = max_eval
        return max_eval



    def min_only_eval(self, game, depth, alpha, beta):
        '''Alpha-beta function for the minimizing player.
           Human minimizes'''
        if depth == 0 or game.winner != None:
            return self.evaluate(game)
        min_eval = self.inf
        for game_after_one_move in self.get_all_moves(game):
            evaluation = self.max_only_eval(game_after_one_move, depth-1, alpha, beta)
            if evaluation < min_eval:
                min_eval = evaluation
            if min_eval <= alpha:
                return min_eval
            if min_eval < beta:
                beta = min_eval
        return min_eval


    def board_after_ai_move(self, game):
        return self.alphabeta(deepcopy(game))
    
    def evaluate(self, game):
        d = game.board.player2_pcs_left - game.board.player1_pcs_left
        res = d ** 2 if d >= 0 else -1 * d ** 2
        k = game.board.player2_kings * 0.5 - game.board.player1_kings * 0.5
        res += k# ** 2 if k >= 0 else -1 * k ** 2
        return res
        