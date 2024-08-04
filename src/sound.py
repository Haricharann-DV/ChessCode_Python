import pygame
import os

class Sound:

    def __init__(self):
        self.moveSound = pygame.mixer.Sound(os.path.join('assets/sounds/move.wav'))
        self.captureSound = pygame.mixer.Sound(os.path.join('assets/sounds/capture.wav'))