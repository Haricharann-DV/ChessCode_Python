#This is the main class of this chess python code

import pygame #this pygame is how we render things
import sys

#we are importing the other classes here (* means all same as java)
from const import * 
from game import *
from square import *
from move import *

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger

        while True: #Till events are present this will run(like mouse movement)
            
            game.showBg(screen)
            game.showLastMove(screen)            
            game.showMoves(screen)
            game.showHover(screen)
            game.showPieces(screen)

            if dragger.dragging:
                dragger.updateBlit(screen)

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.updateMouse(event.pos)
                    clickedRow = dragger.mouseY // SQSIZE
                    clickedCol = dragger.mouseX // SQSIZE

                    if board.square[clickedRow][clickedCol].hasPiece():
                        piece = board.square[clickedRow][clickedCol].piece

                        if piece.color == game.nextPlayer:
                            board.calcMoves(piece, clickedRow, clickedCol)
                            dragger.saveInitial(event.pos)
                            dragger.dragPiece(piece)
                            game.showBg(screen)
                            game.showLastMove(screen)
                            game.showMoves(screen)
                            game.showPieces(screen)
                                            
                elif event.type == pygame.MOUSEMOTION:
                    dragger.updateHoverMouse(event.pos)
                    if dragger.dragging:
                        dragger.updateMouse(event.pos)
                        game.showBg(screen)
                        game.showLastMove(screen)
                        game.showMoves(screen)
                        game.showHover(screen)
                        game.showPieces(screen)
                        dragger.updateBlit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.updateMouse(event.pos)
                        releasedRow = dragger.mouseY // SQSIZE
                        releasedCol = dragger.mouseX // SQSIZE

                        initial = Square(dragger.initialRow,dragger.initialCol)
                        final = Square(releasedRow,releasedCol)
                        move = Move(initial,final)

                        if board.validMove(dragger.piece, move):
                            captured = board.square[releasedRow][releasedCol].hasPiece()
                            board.move(dragger.piece, move)
                            game.playSound(captured)
                            game.showBg(screen)
                            game.showPieces(screen)
                            game.nextTurn()

                    dragger.undragPiece()
 
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()  #shows the screen after execution


main = Main()
main.mainloop()