#########################################
# groupe DLBI
# Nabil HAMOUDI
# Essmay TOUANI
# Lauren EDOH COFFI
# Julie VALBERT
# Chloé GODET
# https://github.com/Nabil-hamoudi/Projet_generation-de-terrain
#########################################


########################
# import des librairies

import tkinter as tk
import random
import copy

########################
# Constantes

HAUTEUR = 800
LARGEUR = 1000
NOMBRE_CASE_R = 100
NOMBRE_CASE_C = 100
RAPORT_CASE_R = HAUTEUR / NOMBRE_CASE_R
RAPORT_CASE_C = LARGEUR / NOMBRE_CASE_C
COULEUR_FOND = "black"
COULEUR = ["green", "blue"]

Proba_eau = 0.5
n = 3
Voisin_Max = 13
K = 2
Chunk = [[], []]
#1(0(gauche)/1(droite)) #2(0->(nombre de chunk)) #3(0->(Nombre Case C)) #4(0->(Nombre case R))
#0 => Terre , 1 => Eau
TempChunk = []
screen = [[-1 for i in range(NOMBRE_CASE_R)]for u in range(NOMBRE_CASE_C)]

########################
# fonctions


def quadrillage(LR=1):
    """Génére un terrain de base, un terrain a droite ou un terrain a gauche"""
    #LR = 0,1 ou 3
    #0 => gauche, 1 => Debut, 3 => Droite
    global Chunk, Proba_eau
    LR = [LR//2, LR % 2]
    LR = set(LR)
    for i in LR:
        Chunk[i].append([[-1 for i in range(NOMBRE_CASE_R)]for u in range(NOMBRE_CASE_C)])
        for C in range(NOMBRE_CASE_C):
            for R in range(NOMBRE_CASE_R):
                Ran = random.random()
                if Ran <= Proba_eau:
                    Chunk[i][-1][C][R] = 1
                else:
                    Chunk[i][-1][C][R] = 0
    Correction(LR)


def Correction(LR):
    """Modifie les Case selon leur voisin"""
    global n, Voisin_Max, Chunk
    for k in range(n):
        for i in LR:
            TempChunk = []
            for C, Ch in enumerate(Chunk[i][-1]):
                for R in range(len(Ch)):
                    count = Comptage(C, R, i, LR)
                    if count < Voisin_Max:
                        TempChunk.append([C, R, 0])
                    else:
                        TempChunk.append([C, R, 1])
            for r in TempChunk:
                Chunk[i][-1][r[0]][r[1]] = r[2]


def Comptage(C, R, i, LR):
    """Compte les valeurs des voisin (0 pour terre 1 pour eau)"""
    global NOMBRE_CASE_R, Chunk
    FinalCount = []
    count = CompteK(C, R)
    for n in count:
        # R_temp <= R_max and R_temp >= 0:
        if n[1] >= NOMBRE_CASE_R:
            if LR == {0, 1} and i == 0:
                FinalCount.append([i + 1, 0, n[0], n[1] - NOMBRE_CASE_R])
                #[i, chunk, C, R]
            elif LR != {0, 1}:
                FinalCount.append([i, -1, n[0], n[1] - NOMBRE_CASE_R])
        elif n[1] < 0:
            if LR == {0, 1} and i == 1:
                FinalCount.append([i - 1, 0, n[0], n[1]])
            elif LR != {0, 1}:
                FinalCount.append([i, -1, n[0], n[1]])
        else:
            FinalCount.append([i, 0, n[0], n[1]])
    Nb = 0
    for c in FinalCount:
        Nb += Chunk[c[0]][c[1]-1][c[2]][c[3]]
    return Nb


def CompteK(C, R):
    """recupere les coordonnées des voisins en fonction de K"""
    global K
    compt = [[C, R]]
    res = []
    for i in range(K):
        tempcount = []
        for p in compt:
            Coor = Count(p[0], p[1])
            res.extend(Coor)
            tempcount.extend(Coor)
        compt = copy.deepcopy(tempcount)
    RES = []
    for i in res:
        if i not in RES:
            RES.append(i)
    return RES


def Count(C, R):
    """Sort les coordonnées des voisins direct"""
    global NOMBRE_CASE_R, NOMBRE_CASE_C, Chunk
    count = []
    C_max = NOMBRE_CASE_C - 1
    for o in [x for x in range(9) if x != 4]:
        C_temp = C - 1 + (o // 3)
        R_temp = R - 1 + (o % 3)
        if C_temp >= 0 and C_temp <= C_max:
            count.append([C_temp, R_temp])
    return count


def Colored(LR=1):
    """Crée et modifie les objets dans le canvas"""
    global screen, RAPORT_CASE_C, RAPORT_CASE_R, NOMBRE_CASE_R, NOMBRE_CASE_C, COULEUR
    if LR == 1:
        for C in range(NOMBRE_CASE_C):
            for R in range(NOMBRE_CASE_R // 2):
                temp = R + NOMBRE_CASE_R // 2
                screen[C][R] = canvas.create_rectangle(R * RAPORT_CASE_C, C * RAPORT_CASE_R, (R + 1) * RAPORT_CASE_C, (C + 1) * RAPORT_CASE_R, fill=COULEUR[Chunk[0][-1][C][temp]], outline=COULEUR[Chunk[0][-1][C][temp]])
                #C * RAPORT_CASE_C, R * RAPORT_CASE_R, (C + 1) * RAPORT_CASE_C, (R + 1) * RAPORT_CASE_R,
                temp1 = R
                R = temp
                screen[C][R] = canvas.create_rectangle(R * RAPORT_CASE_C, C * RAPORT_CASE_R, (R + 1) * RAPORT_CASE_C, (C + 1) * RAPORT_CASE_R, fill=COULEUR[Chunk[1][-1][C][temp1]], outline=COULEUR[Chunk[1][-1][C][temp1]])


########################
# programme principal
racine = tk.Tk()
racine.title("GAME")
# création des widgets
canvas = tk.Canvas(racine, bg=COULEUR_FOND, width=LARGEUR, height=HAUTEUR)
quadrillage()
Colored()
# placement des widgets
canvas.grid(row=1, columnspan=3)
# boucle principale
racine.mainloop()
