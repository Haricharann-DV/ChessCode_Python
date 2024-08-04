import pygame

from const import *

class Dragger:

    def __init__(self):
        self.piece = None
        self.mouseX = 0
        self.mouseY = 0
        self.initialRow = 0
        self.initialCol = 0
        self.hoverMouseX = 0
        self.hoverMouseY = 0
        self.dragging = False

    def updateMouse(self, pos):
        self.mouseX, self.mouseY = (pos) # (Xcor, Ycor)

    def updateHoverMouse(self, pos):
        self.hoverMouseX, self.hoverMouseY = (pos)

    def saveInitial(self, pos):
        self.initialRow = pos[1] // SQSIZE
        self.initialCol = pos[0] // SQSIZE

    def dragPiece(self, piece):
        self.piece = piece
        self.dragging = True

    def undragPiece(self):
        self.piece = None
        self.dragging = False

    def updateBlit(self, surface):
        self.piece.setTexture()
        texture = self.piece.texture
        img = pygame.image.load(texture)
        imgCenter = (self.mouseX - 28 , self.mouseY - 28)
        self.piece.textureRect = img.get_rect(center = imgCenter)
        surface.blit(img,imgCenter)