import pygame
from pion import *

class Pion_py(Pion):
    """ //! representation graphique d'un pion.

    Args:
        Pion (Pion): La classe parent Pion
    """

    def __init__(self, couleur:str, position:list, screen, estDame = False):
        """Classe Graphique du pion

        Args:\n
            couleur (str): Couleur du pion;
            position (list): Position du pion;
            screen (Pygame): interface où il doit etre affiché;
            estDame (bool, optional): statut du pion(Dame ou simple Pion). Defaults to False.
        """
        Pion.__init__(self, couleur, position, estDame)
        self.screen = screen
        self.image = pygame.image.load(f"pion_{self.couleur}.png")
        self.screen.blit(self.image, (position[0] * 90, position[1] * 90, self.image.get_width(), self.image.get_height()))

    def afficher_pion(self, pos:list):
        """Affichage graphique du pion

        Args:
            pos (list): liste de deux entiers contenant la position où representer le pion
        """
        self.screen.blit(self.image, (pos[0] * 90, pos[1] * 90, self.image.get_width(), self.image.get_height()))

    def set_dame(self):
        """Methode qui transforme un pion en dame
        """
        self.estDame = True
        self.image = pygame.image.load(f"dame_{self.couleur}.png")