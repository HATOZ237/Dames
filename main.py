# import scrapy
import sys
import math
from PyQt5.QtWidgets import *
from damier import *
import pygame
import os

pygame.init()
pygame.mixer.init()
music = pygame.mixer.Sound("Super Mario Bros. Soundtrack-mc.mp3")  # musique de jeu
mouse = pygame.mixer.Sound("Mouse Click - Free Sound Effect.mp3")  # musique de clic
music.play(0)
choix_sauvegarde = ''

# pygame.mixer.music.play()
'''pion = None
possible_positions = None
positions_bouffe = []
pion1 = None
'''

def init_pygame():
    result = True
    fen.close()
    pygame.init()
    damier = Damier(comboCouleur.currentText(), int(comboCases.currentText()))
    pygame.display.flip()
    # pygame.display.update()
    # print("clicl")
    # petit = pygame.mixer.Sound("dame.mp3")
    while result:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                pos = list(pygame.mouse.get_pos())
                pos_case = [pos[0] // 90, pos[1] // 90]
                ##########################
                test = damier.can_move(pos_case)
                # print("click1")
                # print("click3")
                if damier.pion_is_set and test[0] is not False:
                    mouse.play(0)
                    damier.clean()
                    pion2 = damier.last_pion_set
                    damier.deplacer_pion(pion2, test[0])
                    # print("click4")
                    if test[1] is True:
                        damier.effacer_pion(damier.get_pion([test[2][0] * 90, test[2][1] * 90]))
                        damier.eat = True
                        damier.jouer(pion2)
                    else:
                        damier.change_turn()
                elif damier.pion_is_set and test[0] is False:
                    if damier.click_possible(pos):
                        mouse.play(0)
                        pion = damier.get_pion(pos)
                        # print("click5")
                        damier.set_postions(pion)
                elif damier.pion_is_set is False and damier.click_possible(pos):
                    mouse.play(0)
                    pion = damier.get_pion(pos)
                    # print("click6")
                    damier.set_postions(pion)
        pygame.display.update()
        if not damier.partie_terminee():
            # partie_terminee(False)
            result = False



def depart():
    app1 = QApplication([])
    fen1 = QWidget()
    print("ou")
    fen1.setWindowTitle("!!! QUITER !!!")
    fen1.setFixedSize(500, 300)
    vbox1 = QVBoxLayout()
    hboxa1 = QHBoxLayout()
    hboxa2 = QHBoxLayout()
    print("ou1")
    hboxa2.addWidget(QLabel("Voulez vous sauvegarder avant de quitter ?"))
    accepter = QPushButton("Oui")
    refuser = QPushButton("Non")
    print("ou")
    refuser.clicked.connect(exit)
    accepter.clicked.connect(save)
    hboxa1.addWidget(accepter)
    print("ou")
    hboxa1.addWidget(refuser)
    vbox1.addLayout(hboxa1)
    vbox1.addLayout(hboxa2)
    fen1.setLayout(vbox1)
    print("ou")
    fen1.show()
    print("ou")
    os.wait3(100)
    print("ou3")
    app1.exec_()

def save():
    print("Sauvegarde reussie")
    exit()

# initialisation

app = QApplication([])
fen = QWidget()
fen.setWindowTitle("Dames")
fen.setFixedSize(350, 300)
vbox = QVBoxLayout()
hboxa = QHBoxLayout()
hboxb = QHBoxLayout()
hboxc = QHBoxLayout()
comboCouleur = QComboBox()
comboCouleur.addItem("noir")
comboCouleur.addItem("blanc")
hboxa.addWidget(QLabel("Choisissez votre couleur: "))
hboxa.addWidget(comboCouleur)
comboCases = QComboBox()
comboCases.addItem("64")
comboCases.addItem("100")
comboCases.addItem("144")
hboxb.addWidget(QLabel("Taille du damier: "))
hboxb.addWidget(comboCases)
commencer = QPushButton("commencer")
sortir = QPushButton("Quitter")
commencer.clicked.connect(init_pygame)
sortir.clicked.connect(exit)
hboxc.addWidget(commencer)
hboxc.addWidget(sortir)
vbox.addLayout(hboxa)
vbox.addLayout(hboxb)
vbox.addLayout(hboxc)
#vbox.addWidget(commencer)
#vbox.addWidget(sortir)
fen.setLayout(vbox)
fen.show()
app.exec_()

##############################################################


##############################################################################################
"""if damier.secondClick != True:
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
                            damier.secondClick = False"""
