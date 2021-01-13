from pion_pygame import *
from math import sqrt


class Damier:

    def __init__(self, couleur: str, nbrecase: int):
        """Classe Graphique du Damier

        Args:\n
            couleur (str): couleur du joueur
            nbrecase (int): nombre de cases
        """
        if couleur.lower() == "blanc" or couleur.lower() == "noir":# la couleur doit etre noir ou blanc
            self.couleur = couleur.lower()
        else:
            raise DamierException("COULEUR INVALIDE")
        if nbrecase == 64 or nbrecase == 100: # seuls le mode en 64 cases et 100 cases sont disponibles
            self.nbrecase = nbrecase
            me = int(sqrt(self.nbrecase))
        else:
            raise DamierException("Nombre invalide")

        self.Listerobot = []#liste des pions du joueur adverse ou du robot
        self.Listejoueur = []# votre liste
        self.GrenierRobot = []#liste des pions devorés pas 
        self.GrenierJoueur = []
        self.ListeDamier = []
        self.GrenierDamier = []
        self.casesOccupable = []

        for x in range(me):
            for y in range(me):
                if y % 2 == 0 and x % 2 == 0:
                    self.casesOccupable.append([x, y])
                if y % 2 != 0 and x % 2 != 0:
                    self.casesOccupable.append([x, y])

        self.caseSize = 90

        self.size = int(sqrt(self.nbrecase)) * self.caseSize

        self.backgroundFen = 203, 155, 128

        self.bouffe2 = False
        self.bouffepion = None

        self.screen = pygame.display.set_mode((self.size, self.size))
        self.screen.fill(self.backgroundFen)
        pygame.display.set_caption("Dames")

        y = 0
        line = 0

        while y < self.size:
            if line % 2 != 0:
                x = 90
            else:
                x = 0
            while x < self.size:
                pygame.draw.rect(self.screen, (80, 80, 80),
                                 (x, y, self.caseSize, self.caseSize))
                x = x + (self.caseSize * 2)
            y = y + self.caseSize
            line = line + 1

        if self.couleur == "blanc":

            for x in range(me):
                for y in range(me // 2 + 1, me):
                    if y % 2 == 0 and x % 2 == 0:
                        self.Listejoueur.append(
                            Pion_py(self.couleur, [x, y], self.screen))
                    if y % 2 != 0 and x % 2 != 0:
                        self.Listejoueur.append(
                            Pion_py(self.couleur, [x, y], self.screen))

            for x in range(me):
                for y in range(me // 2 - 1):
                    if y % 2 == 0 and x % 2 == 0:
                        self.Listerobot.append(
                            Pion_py("noir", [x, y], self.screen))
                    if y % 2 != 0 and x % 2 != 0:
                        self.Listerobot.append(
                            Pion_py("noir", [x, y], self.screen))

        elif self.couleur == "noir":
            for x in range(me):
                for y in range(me // 2 + 1, me):
                    if y % 2 == 0 and x % 2 == 0:
                        self.Listejoueur.append(
                            Pion_py(self.couleur, [x, y], self.screen))
                    if y % 2 != 0 and x % 2 != 0:
                        self.Listejoueur.append(
                            Pion_py(self.couleur, [x, y], self.screen))

            for x in range(me):
                for y in range(me // 2 - 1):
                    if y % 2 == 0 and x % 2 == 0:
                        self.Listerobot.append(
                            Pion_py("blanc", [x, y], self.screen))
                        self.casesOccupable.append([x, y])
                    if y % 2 != 0 and x % 2 != 0:
                        self.Listerobot.append(
                            Pion_py("blanc", [x, y], self.screen))
                        self.casesOccupable.append([x, y])

        self.ListeDamier.extend(self.Listejoueur)
        self.ListeDamier.extend(self.Listerobot)
        self.turn = 1  # 1 pour le joueur et 2 pour le robot
        self.turnCouleur = self.couleur
        self.secondClick = False

    def deplacer_pion(self, pion: Pion_py, pos: list):
        """[summary]

        Args:
            pion (Pion_py): [description]
            pos (list): [description]
        """

        pygame.draw.rect(self.screen, (80, 80, 80), (
            pion.position[0] * 90, pion.position[1] * 90, self.caseSize, self.caseSize))
        # efface la derniere position du pion
        pion.position = pos  # modifie la position du pion
        # vérifie si le pion est a l'opposé du plateau
        if (pion.couleur == self.couleur and pion.position[1] == 0) or ():
            pion.set_dame()  # transmorme le pion en dame
        elif pion.couleur != self.couleur and pion.position[1] == sqrt(self.nbrecase) - 1:
            pion.set_dame()
        # affiche le pion
        pion.afficher_pion(pos)

    def effacer_pion(self, pion):
        """[summary]

        Args:
            pion ([type]): [description]
        """
        print(pion.position)
        pygame.draw.rect(self.screen, (80, 80, 80), (
            pion.position[0] * 90, pion.position[1] * 90, self.caseSize, self.caseSize))
        self.GrenierDamier.append(pion)
        if pion.couleur == self.couleur:
            self.GrenierJoueur.append(pion)
            self.Listejoueur.remove(pion)
        else:
            self.GrenierRobot.append(pion)
            self.Listerobot.remove(pion)
        self.ListeDamier.remove(pion)

    def get_pion(self, pos):
        """[summary]

        Args:
            pos ([type]): [description]

        Returns:
            [type]: [description]
        """
        pos_case = [pos[0] // 90, pos[1] // 90]
        for p in self.ListeDamier:
            if p.position == pos_case:
                return p
        return None

    def click_possible(self, pos: list):
        """[summary]

        Args:
            pos ([type]): [description]

        Returns:
            [type]: [description]
        """
        possible = False
        pos_case = [pos[0] // 90, pos[1] // 90]

        possible = False
        if pos_case in self.casesOccupable:
            occ = self.occuped_position(pos_case)
            if isinstance(occ, list):
                if occ[0] and occ[1] == self.turnCouleur:
                    possible = True

        if self.bouffe2:
            if self.bouffepion.position == pos_case:
                possible = True
            else:
                possible = False

        return possible

    def occuped_position(self, position):
        """[summary]

        Args:
            position ([type]): [description]

        Returns:
            [type]: [description]
        """
        a, b = position
        if a > sqrt(self.nbrecase):
            return True
        if a < 0:
            return True
        if b > sqrt(self.nbrecase):
            return True
        if b < 0:
            return True
        liste_sortie = [True, "blanc"]
        trouve = False
        for x in self.ListeDamier:
            if x.position == position:
                trouve = True
                liste_sortie = [True, x.couleur]
                break
        if trouve:
            return liste_sortie
        if position not in self.casesOccupable:
            trouve = True
        return trouve

    """"""

    def partie_terminee(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        if len(self.Listerobot) == 0:
            return (True, "Joueur")
        if len(self.Listejoueur) == 0:
            return (True, "Robot")
        else:
            return (False, "")

    def jouer(self):
        """[summary]

        Raises:
            DamierException: [description]
        """
        if self.partie_terminee()[0]:
            raise DamierException(" Partie_terminee")

    def change_turn(self):
        """
        docstring
        """
        if self.turnCouleur == "noir":
            self.turnCouleur = "blanc"
        else:
            self.turnCouleur = "noir"

    def give_position(self, pion: Pion):
        """

        :param pion:
        :return:
        """
        possible_position = []
        a, b = pion.position
        if pion.estDame:
            c, d = a, b
            result = True
            while result:
                c = c + 1
                d = d + 1
                test = self.occuped_position([c, d])
                if test == True:
                    result = False
                elif test == False:
                    possible_position.append([[c, d], False, []])
                else:
                    if test[1] != pion.couleur:
                        if self.occuped_position([c + 1, d + 1]) == False:
                            possible_position.append(
                                [[c + 1, d + 1], True, [c, d]])
                        else:
                            result = False
            c, d = a, b
            result = True
            while result:
                c = c - 1
                d = d + 1
                test = self.occuped_position([c, d])
                if test == True:
                    result = False
                elif test == False:
                    possible_position.append([[c, d], False, []])
                else:
                    if test[1] != pion.couleur:
                        if self.occuped_position([c - 1, d + 1]) == False:
                            possible_position.append(
                                [[c - 1, d + 1], True, [c, d]])
                        else:
                            result = False

            c, d = a, b
            result = True
            while result:
                c = c - 1
                d = d - 1
                test = self.occuped_position([c, d])
                if test == True:
                    result = False
                elif test == False:
                    possible_position.append([[c, d], False, []])
                else:
                    if test[1] != pion.couleur:
                        if self.occuped_position([c - 1, d - 1]) == False:
                            possible_position.append(
                                [[c - 1, d - 1], True, [c, d]])
                        else:
                            result = False

            c, d = a, b
            result = True
            while result:
                c = c + 1
                d = d - 1
                test = self.occuped_position([c, d])
                if test:
                    result = False
                elif test is False:
                    possible_position.append([[c, d], False, []])
                else:
                    if test[1] != pion.couleur:
                        if self.occuped_position([c + 1, d - 1]) is False:
                            possible_position.append(
                                [[c + 1, d - 1], True, [c, d]])
                        else:
                            result = False
        else:
            test_ne = self.occuped_position([a + 1, b - 1])
            test_ner = self.occuped_position([a + 2, b - 2])

            test_no = self.occuped_position([a - 1, b - 1])
            test_nor = self.occuped_position([a - 2, b - 2])

            test_so = self.occuped_position([a - 1, b + 1])
            test_sor = self.occuped_position([a - 2, b + 2])

            test_se = self.occuped_position([a + 1, b + 1])
            test_ser = self.occuped_position([a + 2, b + 2])

            if pion.couleur == self.couleur:
                if test_ne is False:
                    possible_position.append([[a + 1, b - 1], False, []])
                elif test_ne is True:
                    pass
                elif test_ne[1] != pion.couleur and test_ner is False:
                    possible_position.append([[a + 2, b - 2], True, [a + 1, b - 1]])

                if test_no is False:
                    possible_position.append([[a - 1, b - 1], False, []])
                elif test_no is True:
                    pass
                elif test_no[1] != pion.couleur and test_nor is False:
                    possible_position.append([[a - 2, b - 2], True, [a - 1, b - 1]])

                if isinstance(test_se, list) and test_se[1] != pion.couleur:
                    if test_ser is False:
                        possible_position.append([[a + 2, b + 2], True, [a + 1, b + 1]])

                if isinstance(test_so, list) and test_so[1] != pion.couleur:
                    if test_sor is False:
                        possible_position.append([[a - 2, b + 2], True, [a - 1, b + 1]])
            else:
                if test_se is False:
                    possible_position.append([[a + 1, b + 1], False, []])
                elif test_ne is True:
                    pass
                elif test_se[1] != pion.couleur and test_ser is False:
                    possible_position.append([[a + 2, b + 2], True, [a + 1, b + 1]])

                if test_so is False:
                    possible_position.append([[a - 1, b + 1], False, []])
                elif test_no is True:
                    pass
                elif test_so[1] != pion.couleur and test_sor is False:
                    possible_position.append([[a - 2, b + 2], True, [a - 1, b + 1]])

                if isinstance(test_ne, list) and test_ne[1] != pion.couleur:
                    if test_ner is False:
                        possible_position.append([[a + 2, b - 2], True, [a + 1, b - 1]])

                if isinstance(test_no, list) and test_no[1] != pion.couleur:
                    if test_nor is False:
                        possible_position.append([[a - 2, b - 2], True, [a - 1, b - 1]])

        return possible_position


"""def nord_ouest(pos_pion, pos):
    a, b = pos_pion
    x, y = pos
    if [a-1, b-1] == [x, y]:
        return True
    else:
        return False


def nord_est(pos_pion, pos):
    a, b = pos_pion
    x, y = pos
    if [a+1, b-1] == [x, y]:
        return True
    else:
        return False


def sud_ouest(pos_pion, pos):
    a, b = pos_pion
    x, y = pos
    if [a-1, b+1] == [x, y]:
        return True
    else:
        return False


def sud_est(pos_pion, pos):
    a, b = pos_pion
    x, y = pos
    if [a+1, b+1] == [x, y]:
        return True
    else:
        return False


def orient(pos_pion, pos):
    lettre = ""
    if nord_est(pos_pion, pos):
        lettre = "NE"
    elif nord_ouest(pos_pion, pos):
        lettre = "NO"
    elif sud_est(pos_pion, pos):
        lettre = "SE"
    elif sud_ouest(pos_pion, pos):
        lettre = "SO"
    return lettre
"""
"""def enabled_position(self, pion: Pion_py):
        [summary]

        Args:
            pion (Pion_py): [description]

        Returns:
            [type]: [description]
        
        possible_position = []
        a, b = pion.position
        xtest = None
        if pion.estDame:
            test = pion.give_possible_positions()
            if isinstance(test, list):
                return possible_position

            else:
                if "NE" in test:  # si la dame peut se deplacer au nord-est du damier
                    xtest = None
                    for x in test["NE"]:
                        # je verifie si la prochaine case dans la direction est possible
                        verify = self.occuped_position(x)
                        if verify == False:
                            possible_position.append([x, False, []])
                            xtest = x  # je stocke la case precedente que je viens d'ajouter
                        elif verify == True:  # le deplacement n'est pas possible dans cette direction donc je sors de la boucle
                            break
                        elif verify is not True:  # dans ce cas, il y a un pion qui gene
                            if xtest is None:  # dans ce cas, la case genante suit celle de la dame
                                # si cette case n'est pas de ma couleur
                                if verify[1] != pion.couleur:
                                    # je verifie donc la case une fois plus loin
                                    if self.occuped_position([a+2, b-2]) == False:
                                        possible_position.append(
                                            [[a+2, b-2], True, [a+1, b-1]])  # je l'ajoute
                                        break  # je sors de la boucle
                            else:  # dans ce cas, la case genante est loin de la dame
                                if verify[1] != pion.couleur:  # si cette case
                                    # je me sers de xtest qui a stocké la derniere position proche de celle de case genante
                                    if self.occuped_position([xtest[0]+2, xtest[1]-2]):
                                        possible_position.append(
                                            [[xtest[0]+2, xtest[1]-2], True, [xtest[0]+1, xtest[1]-1]])
                                        break
                if "NO" in test:
                    xtest = None
                    for x in test["NO"]:
                        verify = self.occuped_position(x)
                        if verify == False:
                            possible_position.append([x, False, []])
                            xtest = x
                        elif verify == True:
                            break
                        elif verify is not True:
                            if xtest is None:
                                if verify[1] != pion.couleur:
                                    if self.occuped_position([a-2, b-2]) == False:
                                        possible_position.append(
                                            [[a-2, b-2], True, [a+1, b-1]])
                                        break
                            else:
                                if verify[1] != pion.couleur:  # si cette case
                                    # je me sers de xtest qui a stocké la derniere position proche de celle de case genante
                                    if self.occuped_position([xtest[0]+2, xtest[1]-2]):
                                        possible_position.append(
                                            [[xtest[0]-2, xtest[1]-2], True, [xtest[0]-1, xtest[1]-1]])
                                        break
                if "SO" in test:
                    xtest = None
                    for x in test["SO"]:
                        verify = self.occuped_position(x)
                        if verify == False:
                            possible_position.append([x, False, []])
                            xtest = x
                        elif verify == True:
                            break
                        elif verify is not True:
                            if xtest is None:
                                if verify[1] != pion.couleur:
                                    if self.occuped_position([a+2, b-2]) == False:
                                        possible_position.append(
                                            [[a-2, b+2], True, [a-1, b+1]])
                                        break
                            else:
                                if verify[1] != pion.couleur:  # si cette case
                                    # je me sers de xtest qui a stocké la derniere position proche de celle de case genante
                                    if self.occuped_position([xtest[0]-2, xtest[1]+2]):
                                        possible_position.append(
                                            [[xtest[0]-2, xtest[1]+2], True, [xtest[0]-1, xtest[1]+1]])
                                        break
                if "SE" in test:
                    xtest = None
                    for x in test["SE"]:
                        verify = self.occuped_position(x)
                        if verify == False:
                            possible_position.append([x, False, []])
                            xtest = x
                        elif verify == True:
                            break
                        elif verify is not True:
                            if xtest is None:
                                if verify[1] != pion.couleur:
                                    if self.occuped_position([a+2, b+2]) == False:
                                        possible_position.append(
                                            [[a+2, b+2], True, [a+1, b+1]])
                                        break
                            else:
                                if verify[1] != pion.couleur:  # si cette case
                                    # je me sers de xtest qui a stocké la derniere position proche de celle de case genante
                                    if self.occuped_position([xtest[0]+2, xtest[1]+2]):
                                        possible_position.append(
                                            [[xtest[0]+2, xtest[1]+2], True, [xtest[0]+1, xtest[1]+1]])
                                        break
        else:
            if pion.couleur == self.couleur:
                if isinstance(self.occuped_position([a-1, b-1]), list):
                    if self.occuped_position([a-1, b-1])[1] != self.couleur:
                        if self.occuped_position([a-2, b-2]) == False:
                            possible_position.append(
                                [[a-2, b-2], True, [a-1, b-1]])
                elif self.occuped_position([a-1, b-1]) == False:
                    possible_position.append([[a-1, b-1], False, []])
                if self.occuped_position([a+1, b-1]) == False:
                    possible_position.append([[a+1, b-1], False, []])
                elif isinstance(self.occuped_position([a+1, b-1]), list):
                    if self.occuped_position([a+1, b-1])[1] != self.couleur:
                        if self.occuped_position([a+2, b-2]) == False:
                            possible_position.append(
                                [[a+2, b-2], True, [a+1, b-1]])
                if isinstance(self.occuped_position([a-1, b+1]), list) and self.occuped_position([a-1, b+1])[1] != self.couleur:
                    if self.occuped_position([a-2, b+2]) == False:
                        possible_position.append([[a-2, b+2], False, []])
                if isinstance(self.occuped_position([a+1, b+1]), list) and self.occuped_position([a+1, b+1])[1] != self.couleur:
                    if self.occuped_position([a+2, b+2]) == False:
                        possible_position.append([[a+2, b+2], False, []])
            else:
                if isinstance(self.occuped_position([a+1, b+1]), list):
                    if self.occuped_position([a+1, b+1])[1] == self.couleur:
                        if self.occuped_position([a+2, b+2]) == False:
                            possible_position.append(
                                [[a+2, b+2], True, [a+1, b+1]])
                elif self.occuped_position([a+1, b+1]) == False:
                    possible_position.append([[a+1, b+1], False, []])

                if isinstance(self.occuped_position([a-1, b+1]), list):
                    if self.occuped_position([a-1, b+1])[1] == self.couleur:
                        if self.occuped_position([a-2, b+2]) == False:
                            possible_position.append(
                                [[a-2, b+2], True, [a-1, b+1]])
                elif self.occuped_position([a-1, b+1]) == False:
                    possible_position.append([[a-1, b+1], False, []])

                if isinstance(self.occuped_position([a-1, b-1]), list) and self.occuped_position([a-1, b-1])[1] == self.couleur:
                    if self.occuped_position([a-2, b-2]) == False:
                        possible_position.append([[a-2, b-2], False, []])

                if isinstance(self.occuped_position([a+1, b-1]), list) and self.occuped_position([a+1, b-1])[1] == self.couleur:
                    if self.occuped_position([a+2, b-2]) == False:
                        possible_position.append([[a+2, b-2], False, []])
        return possible_position"""
