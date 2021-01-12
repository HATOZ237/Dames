import pygame
from pion import *

class Pion_py(Pion):

    def __init__(self, couleur:str, position:list, screen, estDame = False):
        Pion.__init__(self, couleur, position, estDame)
        self.screen = screen
        self.image = pygame.image.load(f"pion_{self.couleur}.png")
        self.screen.blit(self.image, (position[0] * 90, position[1] * 90, self.image.get_width(), self.image.get_height()))

    def afficher_pion(self, pos):
        self.screen.blit(self.image, (pos[0] * 90, pos[1] * 90, self.image.get_width(), self.image.get_height()))

    def set_dame(self):
        self.estDame = True
        self.image = pygame.image.load(f"dame_{self.couleur}.png")