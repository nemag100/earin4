import math
from copy import deepcopy
import pygame
from .constants import PLAYER1, PLAYER2, CLASSIC, SQUARED_PAWNS, EXPANSIVE, END_GAME
from .game import Game

class Minmax:
    '''Class for storing the state of the AI player, playing with the min-max algorithm with alpha-beta pruning.
        Contains methods for computing the best move according to the algorithm.'''
    def __init__(self, ai_color, depth=4, heuristic=CLASSIC, adaptive_heuristics=False, king_factor=0.5, player1_factor=1, player2_factor=1, aggresivenes=0.81):
        '''ai_color - color of the AI player controlled by this class
           depth - search depth for min-max algorithm with alpha-beta pruning
           heuristic - heuristic of the AI player controlled by this class
           adaptive_heuristics - flag for using adaptive heuristics for end-game
           king_factor - multiplier for the number of king pieces for CLASSIC heuristic
           player1_factor, player2_factor - multipliers for the numbers of PLAYER1 and PLAYER2 numbers of pieces,
                                            for CLASSIC heuristics
           aggresivenes - multiplier used to determine when to change the heuristics to the last-but-one stage,
                          specified as percentage of the opponent pieces with respect to the number of pieces
                          owned by the player controlled by this class; just for testing'''
        self.ai_color = ai_color
        self.depth = depth
        self.heuristic = heuristic
        self.adaptive_heuristics = adaptive_heuristics
        self.endgame_leader = False # flag raised if the AI player controlled by this class is considered leader in end-game
                                    # used in case of adaptive heuristics, just for testing
        self.king_factor = king_factor
        self.player1_factor = player1_factor
        self.player2_factor = player2_factor
        self.aggresivenes = aggresivenes
        self.__set_human_color() # in case of AI vs. AI, human is the opponent of the player controlled by this class
        self.inf   = math.inf # positive infinity initialization
        self.ninf  = -math.inf # negative infinity initialization

    def __set_human_color(self):
        '''Sets the color of the human player based on the AI player color.'''
        if self.ai_color == PLAYER1:
            self.human_color = PLAYER2
        else:
            self.human_color = PLAYER1

    def get_all_moves(self, game):
        '''Returns game state for each of the moves possible for the game state given in argument.'''
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
        '''Checks which heuristics to use, then initializes the min-max algorithm with alpha-beta pruning.'''
        if self.adaptive_heuristics: # choose the heuristics if adaptive heuristics flag is raised
            if game.board.get_number_of_pieces(self.human_color) < game.board.get_number_of_pieces(self.ai_color) * self.aggresivenes:
                if not game.board.are_all_kings(self.ai_color):
                    print("entering end game")
                    self.heuristic = EXPANSIVE
                elif game.board.are_all_kings():
                    print("in end game")
                    self.heuristic = END_GAME
                    self.endgame_leader = True
            if game.board.most_are_kings():
                print("in end game")
                self.heuristic = END_GAME
                if game.board.get_number_of_pieces(self.human_color) < game.board.get_number_of_pieces(self.ai_color):
                    self.endgame_leader = True
            if self.endgame_leader and game.board.get_number_of_pieces(self.human_color) >= game.board.get_number_of_pieces(self.ai_color):
                print("ended leadership")
                self.heuristic = CLASSIC
                self.endgame_leader = False
        return self.alphabeta(game) # by default returns the game state given by the min-max algorithm with alpha-beta pruning

    def alphabeta(self, game):
        '''Computes the state of the game after the move recommended by the min-max algorithm with alpha-beta pruning.'''
        if not self.endgame_leader:
            if game.turn == PLAYER1:
                print("human")
                _, best_move = self.min_alphabeta(game, self.depth, self.ninf, self.inf)
            elif game.turn == PLAYER2:
                print("ai")
                _, best_move = self.max_alphabeta(game, self.depth, self.ninf, self.inf)
        else: # the end-game leader heuristic is different and assumes minimization
            _, best_move = self.min_alphabeta(game, self.depth, self.ninf, self.inf)
        return best_move

    def max_alphabeta(self, game, depth, alpha, beta):
        '''Alpha-beta function for the maximizing player.'''
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
        '''Alpha-beta function for the minimizing player.'''
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
            Returns only the evaluation of the game state, and not proposed game state itself, for program
            optimization purposes.'''
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
            Returns only the evaluation of the game state, and not proposed game state itself, for program
            optimization purposes.'''
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
        '''Simulates AI move.'''
        return self.tune_strategy(game).last_move

    def board_after_ai_move(self, game):
        '''Returns the state of the board after AI move.'''
        return self.tune_strategy(deepcopy(game))

    def classic_heuristic(self, game):
        '''Evaluates the game state using classic heuristics.
            Classic means the result is the sum of:
            d - difference between numbers of pieces of both players, multiplied by some factors (defaultly by 1 and 1)
            k - difference between numbers of kings pieces of both players, multiplied by some factor (defaultly by 0.5)'''
        d = game.board.player2_pcs_left * self.player2_factor - game.board.player1_pcs_left * self.player1_factor
        res = d
        k = game.board.player2_kings * self.king_factor - game.board.player1_kings * self.king_factor
        res += k
        return res

    def squared_pawns_heuristic(self, game):
        '''Evaluates the game state using squared_pawns heuristics.
            It is the same as classic heuristics, but the difference d is squared, with the sign preserved.'''
        d = game.board.player2_pcs_left * self.player2_factor - game.board.player1_pcs_left * self.player1_factor
        res = d ** 2 if d >= 0 else -1 * d ** 2
        k = game.board.player2_kings * self.king_factor - game.board.player1_kings * self.king_factor
        res += k
        return res

    def expansive_heuristic(self, game):
        '''Evaluates the game state using expansive heuristics.
            Each piece is assigned a value, based on a constant and the row number, from the point of view
            of the starting edge. The constant for the king is greater, so having a king is biased.'''
        p1_val = 0
        p2_val = 0
        for piece in game.board.get_player_pieces(PLAYER1):
            p1_val += 5 + piece.row if not piece.king else 7 + piece.row
        for piece in game.board.get_player_pieces(PLAYER2):
            p2_val += 5 + (7 - piece.row) if not piece.king else 7 + (7 - piece.row)
        return p2_val - p1_val

    def end_game_heuristic(self, game):
        '''Just for adaptive heuristics. Evaluates the game state using end-game heuristics.
            For each king piece of the end-game leader, distances to the other player pieces are summed up.
            The leader minimizes, because they want to chase the opponent.'''
        sum_of_distances = 0
        for a in game.board.get_player_pieces(self.ai_color):
            if a.king:
                for h in game.board.get_player_pieces(self.human_color):
                    sum_of_distances += a.cartesian(h)
        return sum_of_distances

    def evaluate(self, game):
        '''Evaluates the heuristic value for the game state given in an argument.'''
        if self.heuristic == CLASSIC:
            return self.classic_heuristic(game)
        elif self.heuristic == SQUARED_PAWNS:
            return self.squared_pawns_heuristic(game)
        elif self.heuristic == EXPANSIVE:
            return self.expansive_heuristic(game)
        elif self.heuristic == END_GAME:
            return self.end_game_heuristic(game)
