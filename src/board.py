from const import *
from square import *
from piece import *
from move import *
from castlingPos import *
import copy

class Board:

    def __init__(self):
        self.square= [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self.castlingPos = CastlingPos()
        self._create()
        self._addPieces('white')
        self._addPieces('black')
        self.lastMove = None
        self.lastMovedPiece = None
        self.moveWasEnPassant = False
        self.pawnWasPromoted = False
        self.promotedSquare = None

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.square[col][row]= Square(row,col)

    def move (self, piece, move):
        initial = move.initial
        final = move.final

        enPassantHapp = self.square[final.row][final.col].isEmpty()

        self.square[initial.row][initial.col].piece = None
        self.square[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            self.checkEnPassant(piece, move ,enPassantHapp)
            self.checkPromotion(piece, move)

        if isinstance(piece, King):
            if self.castling(initial.col,final.col):
                diff = initial.col - final.col
                if diff < 0:
                    if self.square[initial.row][7].hasPiece():
                        rookC = self.square[initial.row][7].piece
                        initialR = Square(initial.row,7)
                        finalR = Square(initial.row,5)
                        rookMove = Move(initialR, finalR)
                        self.move(rookC, rookMove)
                elif diff > 0:
                    if self.square[initial.row][0].hasPiece():
                        rookC = piece.leftRook
                        initialR = Square(initial.row,0)
                        finalR = Square(initial.row,3)
                        rookMove = Move(initialR, finalR)
                        self.move(rookC, rookMove)

        piece.moved = True

        for row in range(ROWS):
            for col in range(COLS):
                if self.square[row][col].hasPiece():
                    tempPiece = self.square[row][col].piece
                    tempPiece.clearMoves()

        self.castlingPos.clearCastlingAttacks()
        self.lastMove = move
        self.lastMovedPiece = piece

    def validMove(self, piece, move):
        return move in piece.moves
    
    def checkPromotion(self, piece, move):
        if move.final.row == 0 or move.final.row == 7:
            self.pawnWasPromoted = True
            self.promotedSquare = Square(move.final.row,move.final.col,piece)
    
    def checkPawnWasPromoted(self):
        return self.pawnWasPromoted

    def clearPawnWasPromoted(self):
         self.pawnWasPromoted = False
         self.promotedSquare = None
    
    def checkEnPassant(self, piece, move,enPassantHapp):
        initialEn = move.initial
        finalEn = move.final
        if initialEn.col != finalEn.col and enPassantHapp:
            self.square[initialEn.row][finalEn.col].piece = None
            self.moveWasEnPassant = True
    
    def checkMoveWasEnPassant(self):
        return self.moveWasEnPassant

    def clearMoveWasEnPassant(self):
        self.moveWasEnPassant = False

    def castling(self, initialCol, finalCol):
        return abs(initialCol - finalCol) == 2
    
    def inCheck(self, piece, move):
        tempPiece = copy.deepcopy(piece)
        tempBoard = copy.deepcopy(self)
        rookRow = 7 if tempPiece.color == 'white' else 0

        if isinstance(tempPiece, King):
            for row in range(ROWS):
                for col in range(COLS):
                    if tempBoard.square[row][col].hasEnemyPiece(tempPiece.color):
                        tp = tempBoard.square[row][col].piece
                        tempBoard.calcMoves(tp,row,col,checkFlag=2)
                        for tm in tp.moves:
                            if isinstance(tempBoard.square[tm.final.row][tm.final.col].piece, King):
                                self.castlingPos.kingInCheck(True)
                            if (tm.final.row == rookRow) and (tm.final.col == 5):
                                self.castlingPos.kingSide(True)
                            if (tm.final.row == rookRow) and (tm.final.col == 3):
                                self.castlingPos.QueenSide(True)

        tempBoard.move(tempPiece,move)

        for row in range(ROWS):
            for col in range(COLS):
                if tempBoard.square[row][col].hasEnemyPiece(tempPiece.color):
                    tp = tempBoard.square[row][col].piece
                    tempBoard.calcMoves(tp,row,col,checkFlag=2)
                    for tm in tp.moves:
                        if isinstance(tempBoard.square[tm.final.row][tm.final.col].piece, King):
                            return True
        return False

    def calcMoves(self, piece, row, col, checkFlag=1):

        def pawnMoves():
            steps = 1 if piece.moved else 2
            #normal moves
            start = row + piece.dir
            end = row + (piece.dir*(1+steps))
            for possibleMoveRow in range(start, end, piece.dir):
                if Square.inRange(possibleMoveRow):
                    if self.square[possibleMoveRow][col].isEmpty():
                        self.addValidMoves(piece,row,col,possibleMoveRow,col,checkFlag)
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
                        self.addValidMoves(piece, row, col, possibleMoveRow, possibleMoveCol,checkFlag)            
            #en passant
            if isinstance(self.lastMovedPiece, Pawn):
                lastMoveInitial = self.lastMove.initial
                lastMoveFinal = self.lastMove.final
                if abs(lastMoveInitial.row -lastMoveFinal.row) == 2:
                    if lastMoveFinal.row == row and lastMoveFinal.col == col+1:
                        self.addValidMoves(piece,row,col,(row+piece.dir),col+1,checkFlag)
                    if lastMoveFinal.row == row and lastMoveFinal.col == col-1:
                        self.addValidMoves(piece,row,col,(row+piece.dir),col-1,checkFlag)

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
                        self.addValidMoves(piece, row, col, possibleMoveRow, possibleMoveCol,checkFlag)

        def straightLineMoves(directions):
            for direction in directions:
                possibleMoveRow, possibleMoveCol = (row+direction[0], col+direction[1])

                while Square.inRange(possibleMoveRow,possibleMoveCol):
                    if self.square[possibleMoveRow][possibleMoveCol].isEmpty():
                        self.addValidMoves(piece, row, col, possibleMoveRow, possibleMoveCol,checkFlag)
                    elif self.square[possibleMoveRow][possibleMoveCol].hasEnemyPiece(piece.color):
                        self.addValidMoves(piece, row, col, possibleMoveRow, possibleMoveCol,checkFlag)
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
                        self.addValidMoves(piece, row, col, possibleMoveRow, possibleMoveCol,checkFlag)
                        
            #castling
            if not piece.moved:
                leftRook = self.square[row][0].piece
                if isinstance(leftRook, Rook):
                    if not leftRook.moved:
                        for c in range(1,4):
                            if self.square[row][c].hasPiece():
                                break
                            if c==3:
                                piece.leftRook = leftRook
                                if checkFlag == 1:
                                    initialK = Square(row,col)
                                    finalK = Square(row,2)
                                    moveK = Move(initialK, finalK)
                                    initialR = Square(row,0)
                                    finalR = Square(row,3)
                                    moveR = Move(initialR, finalR)
                                    if not self.inCheck(piece,moveK) and not self.inCheck(leftRook,moveR):
                                        if self.castlingPos.QueenSideCastling():
                                            piece.addMove(moveK)
                                            leftRook.addMove(moveR) 
                                else:
                                    self.addValidMoves(leftRook,row,0,row,3,checkFlag)
                                    self.addValidMoves(piece,row,col,row,2,checkFlag)
                rightRook = self.square[row][7].piece
                if isinstance(rightRook, Rook):
                    if not rightRook.moved:
                        for c in range(5,7):
                            if self.square[row][c].hasPiece():
                                break
                            if c==6:
                                piece.rightRook = rightRook
                                if checkFlag == 1:
                                    initialK = Square(row,col)
                                    finalK = Square(row,6)
                                    moveK = Move(initialK, finalK)
                                    initialR = Square(row,7)
                                    finalR = Square(row,5)
                                    moveR = Move(initialR, finalR)
                                    if not self.inCheck(piece,moveK) and not self.inCheck(rightRook,moveR):
                                        if self.castlingPos.KingSideCastling():
                                            piece.addMove(moveK)
                                            rightRook.addMove(moveR)
                                else:
                                    self.addValidMoves(rightRook,row,7,row,5,checkFlag)
                                    self.addValidMoves(piece,row,col,row,6,checkFlag)

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

    def addValidMoves(self, piece, row, col, possibleMoveRow, possibleMoveCol,checkFlag):
        initial = Square(row,col)
        final = Square(possibleMoveRow,possibleMoveCol)
        move = Move(initial, final)
        if checkFlag == 1:
            if not self.inCheck(piece,move):
                piece.addMove(move)
        else:
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


