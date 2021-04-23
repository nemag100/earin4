import checkers.tests
from checkers.play import Play
from checkers.constants import PLAYER1, PLAYER2
    
def main():
    play = Play()
   #play.vs_ai(PLAYER2)
    #play.vs_human()
    play.ai_vs_ai()
main()