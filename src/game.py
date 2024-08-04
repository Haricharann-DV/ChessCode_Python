import pygame
import os

from const import *
from board import *
from dragger import *
from sound import *

class Game:

    def __init__(self):
        self.nextPlayer = 'white'
        self.hoveredSquare = None
        self.board = Board()
        self.dragger = Dragger()
        self.sound = Sound()
        self.alphaCols = ('a','b','c','d','e','f','g','h')
        
    #show methods

    def showBg(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row+col) % 2 == 0:
                    color = (234,235,200) #RGB (light green)
                else:
                    color = (119,154,88)  #RGB (dark green)
        
                rect = (col*SQSIZE, row*SQSIZE, SQSIZE,SQSIZE)

                pygame.draw.rect(surface,color,rect)

    
    def showCoordinates(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if col == 0:
                    color = (119,154,88) if row % 2==0 else (234,235,200)
                    label = pygame.font.SysFont('monospace', 12, bold=True).render(str(ROWS-row), 1, color)
                    labelPos = (5, 5 + row * SQSIZE)
                    surface.blit(label, labelPos)

                if row == 7:
                    color = (119,154,88) if (col+1) % 2==0 else (234,235,200)
                    label = pygame.font.SysFont('monospace', 12, bold=True).render(self.alphaCols[col], 1, color)
                    labelPos = (col * SQSIZE + SQSIZE - 12, HEIGHT - 19)
                    surface.blit(label, labelPos)

    def showPieces(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.square[row][col].hasPiece():
                    piece = self.board.square[row][col].piece

                    if piece != self.dragger.piece:
                        img = pygame.image.load(piece.texture)
                        imgCenter  = col * SQSIZE + SQSIZE // 2 , row * SQSIZE + SQSIZE // 2
                        piece.textureRect = img.get_rect(center = imgCenter)
                        surface.blit(img, piece.textureRect)

    def showMoves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                moveColor = (200, 100, 100) if (move.final.row+move.final.col) % 2==0 else (200, 70, 70 )
                moveRect = (move.final.col*SQSIZE, move.final.row*SQSIZE, SQSIZE,SQSIZE)
                pygame.draw.rect(surface,moveColor,moveRect)
    
    def showHover(self, surface):
        hoverRow = self.dragger.hoverMouseY // SQSIZE
        hoverCol = self.dragger.hoverMouseX // SQSIZE
        hoverColor = (180, 180, 180)
        hoverRect = (hoverCol*SQSIZE, hoverRow*SQSIZE, SQSIZE,SQSIZE)
        pygame.draw.rect(surface,hoverColor,hoverRect,width=3)

    def showLastMove(self, surface):
        if self.board.lastMove:
            initial = self.board.lastMove.initial
            final = self.board.lastMove.final
            for pos in (initial,final):
                moveColor = (244, 247, 116) if (pos.row+pos.col) % 2==0 else (172, 195, 44)
                outerBoxColor = (200, 70, 70 ) #(49, 44, 243)
                moveRect = (pos.col*SQSIZE, pos.row*SQSIZE, SQSIZE,SQSIZE)
                pygame.draw.rect(surface,moveColor,moveRect)
                pygame.draw.rect(surface,outerBoxColor,moveRect,width=1)

    def showPromotionChoices(self, surface):
        pawnColor = self.nextPlayer

        moveColor = (66, 186, 189) #if (pos.row+pos.col) % 2==0 else (172, 195, 44)
        outerBoxColor = (49, 44, 243)
        moveRect = (2*SQSIZE, 4*SQSIZE, SQSIZE*4,SQSIZE)
        pygame.draw.rect(surface,moveColor,moveRect)
        pygame.draw.rect(surface,outerBoxColor,moveRect,width=1)

        queenImg = pygame.image.load(os.path.join(f'assets/imgs/{pawnColor}_queen.png'))
        queenImgmgCenter  = 2 * SQSIZE + SQSIZE // 2 , 4 * SQSIZE + SQSIZE // 2
        queenTextureRect = queenImg.get_rect(center = queenImgmgCenter)
        surface.blit(queenImg, queenTextureRect)

        rookImg = pygame.image.load(os.path.join(f'assets/imgs/{pawnColor}_rook.png'))
        rookImgmgCenter  = 3 * SQSIZE + SQSIZE // 2 , 4 * SQSIZE + SQSIZE // 2
        rookTextureRect = rookImg.get_rect(center = rookImgmgCenter)
        surface.blit(rookImg, rookTextureRect)

        bishopImg = pygame.image.load(os.path.join(f'assets/imgs/{pawnColor}_bishop.png'))
        bishopImgmgCenter  = 4 * SQSIZE + SQSIZE // 2 , 4 * SQSIZE + SQSIZE // 2
        bishopTextureRect = bishopImg.get_rect(center = bishopImgmgCenter)
        surface.blit(bishopImg, bishopTextureRect)

        knightImg = pygame.image.load(os.path.join(f'assets/imgs/{pawnColor}_knight.png'))
        knightImgmgCenter  = 5 * SQSIZE + SQSIZE // 2 , 4 * SQSIZE + SQSIZE // 2
        knightTextureRect = knightImg.get_rect(center = knightImgmgCenter)
        surface.blit(knightImg, knightTextureRect)

        


    def handlePromotion(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[1] // SQSIZE
            mouseY = event.pos[0] // SQSIZE
            if mouseY == 2 and mouseX == 4:
                self.board.square[self.board.promotedSquare.row][self.board.promotedSquare.col].piece = Queen(self.board.promotedSquare.piece.color)
            elif mouseY == 3 and mouseX == 4:
                self.board.square[self.board.promotedSquare.row][self.board.promotedSquare.col].piece = Rook(self.board.promotedSquare.piece.color)
            elif mouseY == 4 and mouseX == 4:
                self.board.square[self.board.promotedSquare.row][self.board.promotedSquare.col].piece = Bishop(self.board.promotedSquare.piece.color)
            elif mouseY == 5 and mouseX == 4:
                self.board.square[self.board.promotedSquare.row][self.board.promotedSquare.col].piece = Knight(self.board.promotedSquare.piece.color)
            else:
                return False
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.board.square[self.board.promotedSquare.row][self.board.promotedSquare.col].piece = Queen(self.board.promotedSquare.piece.color)
            elif event.key == pygame.K_2:
                self.board.square[self.board.promotedSquare.row][self.board.promotedSquare.col].piece = Rook(self.board.promotedSquare.piece.color)
            elif event.key == pygame.K_3:
                self.board.square[self.board.promotedSquare.row][self.board.promotedSquare.col].piece = Bishop(self.board.promotedSquare.piece.color)
            elif event.key == pygame.K_4:
                self.board.square[self.board.promotedSquare.row][self.board.promotedSquare.col].piece = Knight(self.board.promotedSquare.piece.color)
            else:           
                return False
            return True
        return False

    def playSound(self, captured = False):
        if captured:
            pygame.mixer.Sound.play(self.sound.captureSound)            
        else:
            pygame.mixer.Sound.play(self.sound.moveSound)

    def nextTurn(self):
        self.nextPlayer = 'white' if self.nextPlayer =='black' else 'black'
    
    def reset(self):
        self.__init__()
