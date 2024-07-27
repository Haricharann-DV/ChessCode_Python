from const import *
from square import *
from piece import *
from move import *

class Board:

    def __init__(self):
        self.square= [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self._create()
        self._addPieces('white')
        self._addPieces('black')
        self.lastMove = None

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.square[col][row]= Square(row,col)

    def move (self, piece, move):
        initial = move.initial
        final = move.final
        self.square[initial.row][initial.col].piece = None
        self.square[final.row][final.col].piece = piece

        piece.moved = True
        piece.clearMoves()

        self.lastMove = move

    def validMove(self, piece, move):
        return move in piece.moves

    def calcMoves(self, piece, row, col):

        def pawnMoves():
            steps = 1 if piece.moved else 2
            #normal moves
            start = row + piece.dir
            end = row + (piece.dir*(1+steps))
            for possibleMoveRow in range(start, end, piece.dir):
                if Square.inRange(possibleMoveRow):
                    if self.square[possibleMoveRow][col].isEmpty():
                        self.addValidMoves(piece,row,col,possibleMoveRow,col)
                    else:break
                else:break
            #captures
            possibleMoves = [
                (row+piece.dir,col-1),
                (row+piece.dir,col+1)
            ]
            for possibleMove in possibleMoves:
                possibleMoveRow , possibleMoveCol = (possibleMove)
                if Square.inRange(possibleMoveRow, possibleMoveCol):
                    if(self.square[possibleMoveRow][possibleMoveCol].hasEnemyPiece(piece.color)):
                        self.addValidMoves(piece, row, col, possibleMoveRow, possibleMoveCol)            
            #en passant

        def knightMoves():
            possibleMoves = [
            (row-2, col+1),
            (row-2, col-1),
            (row+2, col+1),
            (row+2, col-1),
            (row-1, col+2),
            (row-1, col-2),
            (row+1, col+2),
            (row+1, col-2)
            ]
            for possibleMove in possibleMoves:
                possibleMoveRow , possibleMoveCol = (possibleMove)
                if Square.inRange(possibleMoveRow, possibleMoveCol):
                    if(self.square[possibleMoveRow][possibleMoveCol].isEmptyOrEnemy(piece.color)):
                        self.addValidMoves(piece, row, col, possibleMoveRow, possibleMoveCol)

        def straightLineMoves(directions):
            for direction in directions:
                possibleMoveRow, possibleMoveCol = (row+direction[0], col+direction[1])

                while Square.inRange(possibleMoveRow,possibleMoveCol):
                    if self.square[possibleMoveRow][possibleMoveCol].isEmpty():
                        self.addValidMoves(piece, row, col, possibleMoveRow, possibleMoveCol)
                    elif self.square[possibleMoveRow][possibleMoveCol].hasEnemyPiece(piece.color):
                        self.addValidMoves(piece, row, col, possibleMoveRow, possibleMoveCol)
                        break
                    elif self.square[possibleMoveRow][possibleMoveCol].hasTeamPiece(piece.color):
                        break
                    possibleMoveRow=possibleMoveRow + direction[0]
                    possibleMoveCol=possibleMoveCol + direction[1]

        def kingMoves(directions):
            for direction in directions:
                possibleMoveRow, possibleMoveCol = (row+direction[0], col+direction[1])
                if Square.inRange(possibleMoveRow,possibleMoveCol):
                    if self.square[possibleMoveRow][possibleMoveCol].isEmptyOrEnemy(piece.color):
                        self.addValidMoves(piece, row, col, possibleMoveRow, possibleMoveCol)


        if isinstance(piece, Pawn):pawnMoves()
        elif isinstance(piece, Knight):knightMoves()

        elif isinstance(piece, Bishop):
            directions=[
                (1,1),
                (-1,-1),
                (1,-1),
                (-1,1)
            ]
            straightLineMoves(directions)

        elif isinstance(piece, Rook):
            directions=[
                (1,0),
                (-1,0),
                (0,-1),
                (0,1)
            ]
            straightLineMoves(directions)

        elif isinstance(piece, Queen):
            directions=[
                (1,1),
                (-1,-1),
                (1,-1),
                (-1,1),
                (1,0),
                (-1,0),
                (0,-1),
                (0,1)
            ]
            straightLineMoves(directions)

        elif isinstance(piece, King):
            directions=[
                (1,1),
                (-1,-1),
                (1,-1),
                (-1,1),
                (1,0),
                (-1,0),
                (0,-1),
                (0,1)
            ]
            kingMoves(directions)

    def addValidMoves(self, piece, row, col, possibleMoveRow, possibleMoveCol):
        initial = Square(row,col)
        final = Square(possibleMoveRow,possibleMoveCol)
        move = Move(initial, final)
        piece.addMove(move)

    def _addPieces(self,color):
        rowPawn, rowOther = (6, 7) if color == 'white' else (1, 0)

        for col in range(COLS):
            self.square[rowPawn][col] = Square(rowPawn, col, Pawn(color))

        self.square[rowOther][1] = Square(rowOther, 1, Knight(color))
        self.square[rowOther][6] = Square(rowOther, 6, Knight(color))

        self.square[rowOther][2] = Square(rowOther, 2, Bishop(color))
        self.square[rowOther][5] = Square(rowOther, 5, Bishop(color))

        self.square[rowOther][0] = Square(rowOther, 0, Rook(color))
        self.square[rowOther][7] = Square(rowOther, 7, Rook(color))

        self.square[rowOther][3] = Square(rowOther, 1, Queen(color))

        self.square[rowOther][4] = Square(rowOther, 6, King(color))

