import sys

import checkers.tests
from checkers.play import Play
from checkers.constants import PLAYER1, PLAYER2, CLASSIC, SQUARED_PAWNS, EXPANSIVE, END_GAME

def main(args):
    '''
    Usage:
            python main.py [mode [player [heuristic]]]
    '''
    mode = 'pva'
    ai = PLAYER1
    ai_heuristic = SQUARED_PAWNS
    if len(args) == 1:
        mode = args[0]
    elif len(args) == 2:
        mode = args[0]
        ai = PLAYER2 if args[1] == 'player1' else PLAYER1
    elif len(args) == 3: # for advanced tests
        mode = args[0]
        ai = PLAYER2 if args[1] == 'player1' else PLAYER1
        ai_heuristic = args[2] # for advanced tests, see constants.py and minmax.py for explenation

    play = Play()
    if mode == 'pva':       # player vs. AI
        play.vs_ai(ai_PLAYER_color=ai, ai_heuristic=ai_heuristic)
    elif mode == 'pvp':     # player vs. player
        play.vs_human()
    elif mode == 'ava':     # AI vs. AI
        play.ai_vs_ai(PLAYER1_heuristic=EXPANSIVE, PLAYER2_heuristic=EXPANSIVE)
    elif mode == 'apva':    # player vs. AI with adaptive heuristics
        play.vs_ai(ai_PLAYER_color=ai, ai_heuristic=ai_heuristic, adaptive_heuristics=True)
    elif mode == 'aava':    # AI vs. AI with adaptive heuristics
        play.ai_vs_ai(PLAYER1_heuristic=EXPANSIVE, PLAYER2_heuristic=EXPANSIVE, adaptive_heuristics=True)

if __name__ == '__main__':
    main(sys.argv[1:])
