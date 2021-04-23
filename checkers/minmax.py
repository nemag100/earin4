import math
from copy import deepcopy
import pygame
from .constants import PLAYER1, PLAYER2, CLASSIC, SQUARED_PAWNS, EXPANSIVE, END_GAME
from .game import Game

class Minmax:

    def __init__(self, ai_color, depth=4, heuristic=CLASSIC, king_factor=0.5, player1_factor=1, player2_factor=1):
        '''depth - search depth for alpha-beta algorithm
           PLAYER1 minimizes, PLAYER2 maximizes'''
        self.ai_color = ai_color
        self.depth = depth
        self.heuristic = heuristic
        self.king_factor = king_factor
        self.player1_factor = player1_factor
        self.player2_factor = player2_factor
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
        for piece_coords, piece_moves in valid_moves.items():
            for destination in piece_moves.keys():            #for every move
                copied_game = deepcopy(game)       #make a copy of current game
                copied_game.select_piece(*piece_coords) #move the piece
                copied_game.move_piece(*destination)
                                                #save the game after moving
                games_after_one_move.append(copied_game)
        return games_after_one_move

    def tune_strategy(self, game):
        if game.board.get_number_of_pieces(self.human_color) == 1:
            if not game.board.are_all_kings(self.ai_color):
                print("in end game")
                if self.human_color == PLAYER1:
                    self.player1_factor = game.board.get_number_of_pieces(self.ai_color)
                elif self.human_color == PLAYER2:
                    self.player2_factor = game.board.get_number_of_pieces(self.ai_color)
        return self.alphabeta(game)

    def alphabeta(self, game):
        if game.turn == PLAYER1:
            print("human")
            _, best_move = self.min_alphabeta(game, self.depth, self.ninf, self.inf)
        elif game.turn == PLAYER2:
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

    def ai_move(self, game):
        return self.tune_strategy(game).last_move

    def board_after_ai_move(self, game):
        return self.tune_strategy(deepcopy(game))

    def classic_heuristic(self, game):
        d = game.board.player2_pcs_left * self.player2_factor - game.board.player1_pcs_left * self.player1_factor
        res = d
        k = game.board.player2_kings * self.king_factor - game.board.player1_kings * self.king_factor
        res += k
        return res

    def squared_pawns_heuristic(self, game):
        d = game.board.player2_pcs_left * self.player2_factor - game.board.player1_pcs_left * self.player1_factor
        res = d ** 2 if d >= 0 else -1 * d ** 2
        k = game.board.player2_kings * self.king_factor - game.board.player1_kings * self.king_factor
        res += k
        return res

    def expansive_heuristic(self, game):
        '''PLAYER1 minimizes, PLAYER2 maximizes'''
        p1_val = 0
        p2_val = 0
        for piece in game.board.get_player_pieces(PLAYER1):
            p1_val += 5 + piece.row if not piece.king else 7 + piece.row
        for piece in game.board.get_player_pieces(PLAYER2):
            p2_val += 5 + (7 - piece.row) if not piece.king else 7 + (7 - piece.row)
        return p2_val - p1_val

    def end_game_heuristic(self, game):

        sum_of_distances = 0
        for p1 in game.board.get_player_pieces(PLAYER1):
            for p2 in game.board.get_player_pieces(PLAYER2):
                sum_of_distances += p1.cartesian(p2)

    def evaluate(self, game):
        if self.heuristic == CLASSIC:
            return self.classic_heuristic(game)
        elif self.heuristic == SQUARED_PAWNS:
            return self.squared_pawns_heuristic(game)
        elif self.heuristic == EXPANSIVE:
            return self.expansive_heuristic(game)
        elif self.heuristic == END_GAME:
            pass
