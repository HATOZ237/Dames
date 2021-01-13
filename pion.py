import pygame


class DamierException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Pion:

    def __init__(self, couleur: str, position: list, estDame=False):
        """Classe Pion

        Args:\n
            couleur (str): couleur du pion
            position (list): position du pion
            estDame (bool): pion est dame

        Raises:\n
            DamierException: couleur fournie invalide
            DamierException: position fournie invalide
            DamierException: position fournie invalide
        """

        self.couleur = ""
        self.position = []
        self.estDame = False
        if couleur.lower() == "blanc" or couleur.lower() == "noir":
            self.couleur = couleur.lower()
        else:
            raise DamierException("Couleur invalide")

        if isinstance(estDame, bool):
            self.estDame = estDame
        else:
            raise DamierException("valeur estDame invalide")

        if isinstance(position, list):
            if isinstance(position[0], int) or isinstance(position[1], int):
                if position[0] <= 100 and position[0] >= 0 and position[1] <= 100 and position[1] >= 0:
                    self.position = position
                else:
                    raise DamierException("Position invalide")
            else:
                raise DamierException("Position invalide")
        else:
            raise DamierException("Position invalide")

    def __str__(self):
        return f"Couleur: {self.couleur}, Est une dame: {self.estDame}, Coordonnées: {self.position}"

    """def give_possible_positions(self):
        [summary]

        Returns:
            [type]: [description]
    
        liste_possible = []
        a, b = self.position
        c, d = a, b
        if self.estDame is not True:
            for x in [[a+1, b+1], [a-1, b+1], [a+1, b-1], [a-1, b-1]]:
                if(position_valide(x)):
                    liste_possible.append(x)
        else:
            liste = []
            dictio = {}
            c = a-1
            d = b+1
            while position_valide([c, d]):
                liste.append([c, d])
                c = c-1
                d = d+1
            dictio["SO"] = liste
            liste = []
            c = a+1
            d = b-1
            while position_valide([c,d]):
                liste.append([c,d])
                c = c+1
                d = d-1
            dictio["NE"] = liste
            liste = []
            c = a-1
            d = b-1
            while position_valide([c,d]):
                liste.append([c,d])
                c = c-1
                d = d-1
            dictio["NO"] = liste
            liste = []
            c = a+1
            d = b+1
            while position_valide([c,d]):
                liste.append([c,d])
                c = c+1
                d = d+1
            dictio["SE"] = liste
            if len(dictio) > 0: return dictio
        return liste_possible"""

"""def position_valide(position: list):
    a, b = position
    if a < 0 or a > 10:
        return False
    else:
        return True"""
