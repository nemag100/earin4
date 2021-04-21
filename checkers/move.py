class Move:
    '''docstring for Move'''
    def __init__(self):
        self.moves = []
        self.jumps = []
        self.captured = []

    def __eq__(self, other):
        return self.moves == other.moves and self.captured == other.captured and self.jumps==other.jumps
    
    def __ne__(self, other):
        return not self.__eq__(other)

    
    def hop(self, h):
        self.hops.append(h)

    def capture(self, c):
        self.captures.append(c) 
    
    def move(self, m):
        self.moves.append(m)