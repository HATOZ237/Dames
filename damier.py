from pion_pygame import *
from math import sqrt


class Damier:

    def __init__(self, couleur: str, nbrecase: int):
        """Classe Graphique du Damier:\n Il est considéré comme un repere orthonormé dont l'origine est au 
        au coin superieur gauche(par rapport à vous)

        Args:\n
            couleur (str): couleur du joueur
            nbrecase (int): nombre de cases
        """
        if couleur.lower() == "blanc" or couleur.lower() == "noir":  # la couleur doit etre noir ou blanc
            self.couleur = couleur.lower()
        else:
            raise DamierException("COULEUR INVALIDE")
        # seuls le mode en 64 cases et 100 cases sont disponibles
        if nbrecase == 64 or nbrecase == 100 or nbrecase == 144:
            self.nbrecase = nbrecase
            me = int(sqrt(self.nbrecase))
        else:
            raise DamierException("Nombre invalide")

        self.Listerobot = []  # liste des pions du joueur adverse ou du robot
        self.Listejoueur = []  # votre liste
        self.GrenierRobot = []  # liste des pions devorés pas le joueur adverse
        self.GrenierJoueur = []  # liste des pions devorés par le joueur
        self.ListeDamier = []  # liste de tous les pions presents sur le damier
        self.GrenierDamier = []
        # liste des emplacements des cases noirs qui sont les seules considérées
        self.casesOccupable = []
        self.last_pion_set = None
        self.pion_is_set = False
        self.eat = False

        #on recupere les coordonnées des points noirs
        for x in range(me):
            for y in range(me):
                if y % 2 == 0 and x % 2 == 0:
                    self.casesOccupable.append([x, y])
                if y % 2 != 0 and x % 2 != 0:
                    self.casesOccupable.append([x, y])

        self.caseSize = 90

        self.size = int(sqrt(self.nbrecase)) * self.caseSize

        self.backgroundFen = 203, 155, 128#ne pas modifier

        #######################j'ai oublié##############
        self.bouffe2 = False
        self.bouffepion = None
        ######################à quoi ça sert################

        self.screen = pygame.display.set_mode((self.size, self.size))
        self.screen.fill(self.backgroundFen)
        pygame.display.set_caption("Dames : ")

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
        self.last_cases_set = []

    def deplacer_pion(self, pion: Pion_py, pos: list):
        """Deplace le pion à la position donnée en parametre\n

        Args:\n
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

    def effacer_pion(self, pion: Pion_py):
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

    def get_pion(self, pos: list):
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
                if occ[1] == self.turnCouleur:
                    possible = True

        if self.bouffe2:
            if self.bouffepion.position == pos_case:
                possible = True
            else:
                possible = False

        return possible

    def occuped_position(self, position):
        """Fonction qui informe sur l'occupation d'une case sur le damier \n

        Args:
            position (list): Liste de coordonnées de la forme [x,y] x et y étant compris entre 0 et la racine du nombre de case

        Returns:
            True si la case n'existe pas ou ne respecte pas les conditions on dit qu'elle est occupée\n
            False si elle est libre \n
            [True, couleur] si elle est occupée et couleur étant la couleur du pion qui occupe la case
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
        """Renseigne sur l'etat de jeu dans la partie

        Returns:
            tuple: false et "" si la partie n'est pas terminée et true, nom_du_gag
        """
        if len(self.Listerobot) == 0:
            return True, "Joueur"
        if len(self.Listejoueur) == 0:
            return True, "Robot"
        else:
            return (False, "")

    def jouer(self, pion: Pion_py):
        """Cette fonction permet de redefinir les positions du pion à jouer si celui vient de bouffer

        Raises:
            DamierException: [description]
        """
        liste = []
        print(self.last_cases_set)
        if self.eat:
            for p, p1, p2 in self.give_position(pion):
                if p1:
                    liste.append([p, p1, p2])
            if len(liste) != 0:
                self.last_cases_set = liste
                print(self.last_cases_set)
                self.pion_is_set = True
                self.last_pion_set = pion
                for p, p1, p2 in self.last_cases_set:
                    pygame.draw.rect(self.screen, (255, 120, 120), (
                        p[0] * 90, p[1] * 90, self.caseSize, self.caseSize))  # colorie la case en rouge
            else:
                self.change_turn()
            self.eat = False

    def change_turn(self):
        """
        Change le tour de la partie
        """
        if self.turnCouleur == "noir":
            self.turnCouleur = "blanc"
        else:
            self.turnCouleur = "noir"

    def give_position(self, pion: Pion):
        """
        donne les positions du pion ou de la dame vers lesquelles ils peuvent aller
        il s'agit d'une fonction tres complexe mais fonctionnelle
        Ne pas y toucher à moins d'en faire une copie
        PS: ça m'a pris 2 jours d'écrire ça

        :param pion:
        :return: Une liste des futures positions possibles d'un pion
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
                    break

            c, d = a, b
            result = True
            while result:
                c = c - 1
                d = d + 1
                test = self.occuped_position([c, d])
                if test == True:  # ne pas modifier
                    result = False
                elif test == False:  # ne pas modifier
                    possible_position.append([[c, d], False, []])
                else:
                    if test[1] != pion.couleur:
                        if self.occuped_position([c - 1, d + 1]) == False:  # ne pas modifier
                            possible_position.append(
                                [[c - 1, d + 1], True, [c, d]])
                        else:
                            result = False
                    break

            c, d = a, b
            result = True
            while result:
                c = c - 1
                d = d - 1
                test = self.occuped_position([c, d])
                if test == True:#ne pas modifier
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
                    break
            c, d = a, b
            result = True
            while result:
                c = c + 1
                d = d - 1
                test = self.occuped_position([c, d])
                if test == True:#ne pas modifier
                    result = False
                elif test == False:#ne pas modifier
                    possible_position.append([[c, d], False, []])
                else:
                    if test[1] != pion.couleur:
                        if self.occuped_position([c + 1, d - 1]) == False:#ne pas modifier
                            possible_position.append(
                                [[c + 1, d - 1], True, [c, d]])
                        else:
                            result = False
                    break
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
                    possible_position.append(
                        [[a + 2, b - 2], True, [a + 1, b - 1]])

                if test_no is False:
                    possible_position.append([[a - 1, b - 1], False, []])
                elif test_no is True:
                    pass
                elif test_no[1] != pion.couleur and test_nor is False:
                    possible_position.append(
                        [[a - 2, b - 2], True, [a - 1, b - 1]])

                if isinstance(test_se, list) and test_se[1] != pion.couleur:
                    if test_ser is False:
                        possible_position.append(
                            [[a + 2, b + 2], True, [a + 1, b + 1]])

                if isinstance(test_so, list) and test_so[1] != pion.couleur:
                    if test_sor is False:
                        possible_position.append(
                            [[a - 2, b + 2], True, [a - 1, b + 1]])
            else:
                if test_se is False:
                    possible_position.append([[a + 1, b + 1], False, []])
                elif test_ne is True:
                    pass
                elif test_se[1] != pion.couleur and test_ser is False:
                    possible_position.append(
                        [[a + 2, b + 2], True, [a + 1, b + 1]])

                if test_so is False:
                    possible_position.append([[a - 1, b + 1], False, []])
                elif test_no is True:
                    pass
                elif test_so[1] != pion.couleur and test_sor is False:
                    possible_position.append(
                        [[a - 2, b + 2], True, [a - 1, b + 1]])

                if isinstance(test_ne, list) and test_ne[1] != pion.couleur:
                    if test_ner is False:
                        possible_position.append(
                            [[a + 2, b - 2], True, [a + 1, b - 1]])

                if isinstance(test_no, list) and test_no[1] != pion.couleur:
                    if test_nor is False:
                        possible_position.append(
                            [[a - 2, b - 2], True, [a - 1, b - 1]])

        return possible_position

    def set_postions(self, pion: Pion_py):
        """
        docstring
        """

        if self.last_pion_set == pion:  # si le pion touché est le meme deux fois de suite, on desactive ses cases
            for p, p1, p2 in self.last_cases_set:
                pygame.draw.rect(self.screen, (80, 80, 80), (
                    p[0] * 90, p[1] * 90, self.caseSize, self.caseSize))
            self.last_cases_set.clear()  # on reinitialise la liste de derniere position
            self.pion_is_set = False  # le dernier pion est reinitialisé
            self.last_pion_set = None
        else:
            if self.pion_is_set is False:  # si le pion n'a pas encore ete touché, active ses cases
                for p, p1, p2 in self.give_position(pion):
                    pygame.draw.rect(self.screen, (255, 120, 120), (
                        p[0] * 90, p[1] * 90, self.caseSize, self.caseSize))
                    self.last_cases_set.append([p, p1, p2])
                self.pion_is_set = True
                self.last_pion_set = pion
            else:  # le pion touché n'est pas le meme que le précedent, on efface les cases du precedent et on met celles du suivant
                for p, p1, p2 in self.last_cases_set:
                    pygame.draw.rect(self.screen, (80, 80, 80), (
                        p[0] * 90, p[1] * 90, self.caseSize, self.caseSize))
                self.last_cases_set.clear()
                self.last_pion_set = pion
                for p, p1, p2 in self.give_position(pion):
                    pygame.draw.rect(self.screen, (255, 120, 120), (
                        p[0] * 90, p[1] * 90, self.caseSize, self.caseSize))
                    self.last_cases_set.append([p, p1, p2])

    def can_move(self, pos: list):
        for p, p1, p2 in self.last_cases_set:
            if pos == p:
                return [p, p1, p2]
        return [False, False, False]

    def clean(self):
        for p, p1, p2 in self.last_cases_set:
            pygame.draw.rect(self.screen, (80, 80, 80), (
                p[0] * 90, p[1] * 90, self.caseSize, self.caseSize))
        self.last_cases_set.clear()
        self.pion_is_set = False


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
