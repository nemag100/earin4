import sys

import checkers.tests
from checkers.play import Play
from checkers.constants import PLAYER1, PLAYER2

def main(args):
    mode = 'pva'
    ai = PLAYER1
    if len(args) == 1:
        mode = args[0]
    elif len(args) == 2:
        mode = args[0]
        ai = PLAYER2 if args[1] == 'player1' else PLAYER1

    play = Play()
    if mode == 'pva':
        play.vs_ai(ai)
    elif mode == 'pvp':
        play.vs_human()
    elif mode == 'ava':
        play.ai_vs_ai()

if __name__ == '__main__':
    main(sys.argv[1:])
