
class Square:

    def __init__(self,  row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, other):
        return self.col == other.col and self.row == other.row and self.piece == other.piece

    def hasPiece(self):
        return self.piece != None
    
    @staticmethod
    def inRange(*args):
        for arg in args:
            if arg<0 or arg>7:
                return False            
        return True
    
    def isEmpty(self):
        return not self.hasPiece()

    def hasEnemyPiece(self, color):
        return self.hasPiece() and self.piece.color != color
    
    def hasTeamPiece(self, color):
        return self.hasPiece() and self.piece.color == color

    def isEmptyOrEnemy(self, color):
        return self.isEmpty() or self.hasEnemyPiece(color)


  