import sys
import pygame
import math
from PyQt5.QtWidgets import *
from damier import *

pion = None
possible_positions = None
positions_bouffe = []
pion1 = None


def init_pygame():
    fen.close()
    pygame.init()
    damier = Damier(comboCouleur.currentText(), int(comboCases.currentText()))
    pygame.display.flip()
    while damier.partie_terminee():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                print("click")

                pos = pygame.mouse.get_pos()
                pos_case = [pos[0] // 90, pos[1] // 90]

                if damier.secondClick != True:
                    if damier.click_possible(pos):
                        pion = damier.get_pion(pos)

                        possible_positions = damier.give_position(pion)

                        print(possible_positions)
                        pion1 = pion

                        if len(possible_positions) > 0:
                            for possible_pos in possible_positions:
                                print(possible_pos)
                                pygame.draw.rect(damier.screen, (255, 120, 120), (
                                    possible_pos[0][0] * 90, possible_pos[0][1] * 90, damier.caseSize, damier.caseSize))
                            damier.secondClick = True
                elif damier.secondClick:
                    click_pos = False
                    elim_pion = False
                    pion_elim = []
                    for p, p2, p3 in possible_positions:
                        if p == pos_case:
                            click_pos = True
                            elim_pion = p2

                            if elim_pion:
                                pion_elim = p3
                            break

                    if click_pos:

                        for possible_pos in possible_positions:
                            pygame.draw.rect(damier.screen, (80, 80, 80), (
                                possible_pos[0][0] * 90, possible_pos[0][1] * 90, damier.caseSize, damier.caseSize))

                        damier.deplacer_pion(pion, pos_case)

                        print(pion.position)

                        positions_bouffe = []

                        if elim_pion:
                            damier.effacer_pion(damier.get_pion(
                                [pion_elim[0] * 90, pion_elim[1] * 90]))

                            for p, p2, p3 in damier.give_position(pion):
                                # print(p2)
                                if p2:
                                    positions_bouffe.append(p)

                            print(positions_bouffe)

                            if len(positions_bouffe) > 0:
                                damier.bouffe2 = True
                                damier.bouffepion = pion
                            else:
                                damier.change_turn()
                            damier.secondClick = False
                        else:
                            damier.change_turn()
                            damier.secondClick = False
                    """elif damier.click_possible(pos) and click_pos == False:
                        print(1)
                        for p, p1, p2 in damier.give_position(pion1):
                             pygame.draw.rect(damier.screen, (80, 80, 80), (
                                p[0] * 90, p[1] * 90, damier.caseSize, damier.caseSize))
                        for p, p1, p2 in damier.give_position(damier.get_pion(pos)):
                            pygame.draw.rect(damier.screen, (255, 120, 120), (
                                p[0] * 90, p[1] * 90, damier.caseSize, damier.caseSize))"""
        pygame.display.update()


# initialisation

app = QApplication([])
fen = QWidget()
fen.setWindowTitle("Dames")
fen.setFixedSize(350, 300)
vbox = QVBoxLayout()
hboxa = QHBoxLayout()
hboxb = QHBoxLayout()
comboCouleur = QComboBox()
comboCouleur.addItem("noir")
comboCouleur.addItem("blanc")
hboxa.addWidget(QLabel("Choisissez votre couleur: "))
hboxa.addWidget(comboCouleur)
comboCases = QComboBox()
comboCases.addItem("64")
comboCases.addItem("100")
hboxb.addWidget(QLabel("Taille du damier: "))
hboxb.addWidget(comboCases)
commencer = QPushButton("commencer")
commencer.clicked.connect(init_pygame)
vbox.addLayout(hboxa)
vbox.addLayout(hboxb)
vbox.addWidget(commencer)
fen.setLayout(vbox)
fen.show()
app.exec_()
