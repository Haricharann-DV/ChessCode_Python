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

    def playSound(self, captured = False):
        if captured:
            pygame.mixer.Sound.play(self.sound.captureSound)            
        else:
            pygame.mixer.Sound.play(self.sound.moveSound)


    def nextTurn(self):
        self.nextPlayer = 'white' if self.nextPlayer =='black' else 'black'
