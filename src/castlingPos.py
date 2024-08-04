

class CastlingPos:

    def __init__(self, kingIsAttacked = False):
        self.kingIsAttacked = kingIsAttacked
        self.kingSideRookAttacked  = False
        self.QueenSideRookAttacked  = False


    def kingInCheck(self, kingIsAttacked):
        self.kingIsAttacked = kingIsAttacked

    def kingSide(self, kingSideRookAttacked ):
        self.kingSideRookAttacked  = kingSideRookAttacked 

    def QueenSide(self, QueenSideRookAttacked ):
        self.QueenSideRookAttacked  = QueenSideRookAttacked 

    def QueenSideCastling(self):
        return not (self.kingIsAttacked or self.QueenSideRookAttacked)
    
    def KingSideCastling(self):
        return not (self.kingIsAttacked or self.kingSideRookAttacked)
    
    def clearCastlingAttacks(self):
        self.kingIsAttacked = False
        self.kingSideRookAttacked  = False
        self.QueenSideRookAttacked  = False

    