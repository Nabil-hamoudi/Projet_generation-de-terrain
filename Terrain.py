#########################################
# groupe DLBI
# Nabil HAMOUDI
# Essmay TOUAMI
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
import tkinter.messagebox

########################
# Constantes

HAUTEUR = 800
LARGEUR = 1000
NOMBRE_CASE_R = 50
NOMBRE_CASE_C = 50
RAPORT_CASE_R = HAUTEUR / NOMBRE_CASE_R
RAPORT_CASE_C = LARGEUR / NOMBRE_CASE_C
COULEUR_FOND = "black"
COULEUR = ["green", "blue"]

Proba_eau = 0.5
n = 4
Voisin_Max = 5
K = 1
Chunk = [[], []]
#1(0(gauche)/1(droite)) #2(0->(nombre de chunk)) #3(0->(Nombre Case C)) #4(0->(Nombre case R))
#0 => Terre , 1 => Eau
TempChunk = []
screen = [[-1 for i in range(NOMBRE_CASE_R)]for u in range(NOMBRE_CASE_C)]

########################
# Variables globales

personnage = -1 #cercle rouge représentant le personnage
perso = False #indique si le personnage existe
C_perso = -1 #colonne de la case du screen dans laquelle est placé le personnage
R_perso = -1 #ligne de la case du screen dans laquelle est placé le personnage
deplacements = [] #liste des déplacements effectués grâce aux flèches du clavier


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


#fonction Colored de Nabil
""" def Colored(LR=1):
    #Crée et modifie les objets dans le canvas
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
 """



def etat_terrain(C,R):
    """Retourne 0 si c'est une case de terre et 1 si c'est une case d'eau 
    à partir de la colonne et de la ligne de la partie visible"""
    if C < NOMBRE_CASE_C//2:
        etat = Chunk[0][-1][C+NOMBRE_CASE_C//2][R]
    else:
        etat = Chunk[1][-1][C-NOMBRE_CASE_C//2][R]
    return(etat)


def Colored(LR=1):
    """Crée les cases vertes (terre) et bleues (eau)"""
    global screen, RAPORT_CASE_C, RAPORT_CASE_R, NOMBRE_CASE_R, NOMBRE_CASE_C, COULEUR
    if LR == 1:
        for C in range(NOMBRE_CASE_C):
            for R in range(NOMBRE_CASE_R):
                screen[C][R] = canvas.create_rectangle(C*RAPORT_CASE_C, R*RAPORT_CASE_R, (C + 1) * RAPORT_CASE_C, (R + 1) * RAPORT_CASE_R, fill=COULEUR[etat_terrain(C,R)])


def personnage(event):
    """Place le personnage sur la case cliquée et le retire si on clique sur la case dans laquelle il est déjà"""
    global personnage, perso, C_perso, R_perso, deplacements
    if perso == False:
        C_perso = int(event.x // RAPORT_CASE_C)
        R_perso = int(event.y // RAPORT_CASE_R)
        if etat_terrain(C_perso, R_perso) == 0:
            personnage = canvas.create_oval(C_perso*RAPORT_CASE_C+RAPORT_CASE_C/3, R_perso*RAPORT_CASE_R+RAPORT_CASE_R/3, C_perso*RAPORT_CASE_C+2*RAPORT_CASE_C/3, R_perso*RAPORT_CASE_R+2*RAPORT_CASE_R/3, fill="red")
            perso = True
        else:
            tk.messagebox.showwarning(title="Attention !", message="Placez-vous sur une case de terre.", default="ok", icon="warning")
    else:
        if event.x // RAPORT_CASE_C == C_perso and event.y // RAPORT_CASE_R == R_perso:
            canvas.delete(personnage)
            perso = False
            deplacements = []        

            
def deplacement_haut(event):
    """Déplace le personnage d'une case vers le haut si on appuie sur la flèche vers le haut du clavier
    et enregistre le déplacement"""
    global personnage, perso, C_perso, R_perso
    if perso:
        if R_perso > 0:
            if etat_terrain(C_perso, R_perso-1) == 0:
                canvas.move(personnage, 0, -RAPORT_CASE_R)
                R_perso-=1
                deplacements.append("h")


def deplacement_bas(event):
    """Déplace le personnage d'une case vers le bas si on appuie sur la flèche vers le bas du clavier
    et enregistre le déplacement"""
    global personnage, perso, C_perso, R_perso
    if perso:
        if R_perso < NOMBRE_CASE_R - 1:
            if etat_terrain(C_perso, R_perso+1) == 0:
                canvas.move(personnage, 0, RAPORT_CASE_R)
                R_perso+=1
                deplacements.append("b")


def deplacement_gauche(event):
    """Déplace le personnage d'une case vers la gauche si on appuie sur la flèche vers la gauche du clavier
    et enregistre le déplacement"""
    global personnage, perso, C_perso, R_perso
    if perso:
        if C_perso > 0:
            if etat_terrain(C_perso-1, R_perso) == 0:
                canvas.move(personnage, -RAPORT_CASE_C, 0)
                C_perso-=1
                deplacements.append("g")


def deplacement_droite(event):
    """Déplace le personnage d'une case vers la droite si on appuie sur la flèche vers la droite du clavier
    et enregistre le déplacement"""
    global personnage, perso, C_perso, R_perso
    if perso:
        if C_perso < NOMBRE_CASE_C - 1:
            if etat_terrain(C_perso+1, R_perso) == 0:
                canvas.move(personnage, RAPORT_CASE_C, 0)
                C_perso+=1
                deplacements.append("d")


def annule_deplacement(event):
    """Annule le dernier déplacement effectué si on appuie sur Ctrl-z"""
    global deplacements
    if len(deplacements)>0:
        if deplacements[len(deplacements)-1] == "h":
            deplacement_bas(event)
        elif deplacements[len(deplacements)-1] == "b":
            deplacement_haut(event)
        elif deplacements[len(deplacements)-1] == "g":
            deplacement_droite(event)
        elif deplacements[len(deplacements)-1] == "d":
            deplacement_gauche(event)
        deplacements.pop() #suppression du déplacement ajouté par la fonction deplacement appelée ci-dessus
        deplacements.pop() #suppression du déplacement annulé
            

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
canvas.bind('<Button-1>', personnage)
canvas.bind_all("<Up>", deplacement_haut)
canvas.bind_all("<Down>", deplacement_bas)
canvas.bind_all("<Left>", deplacement_gauche)
canvas.bind_all("<Right>", deplacement_droite)
canvas.bind_all("<Control-KeyPress-z>", annule_deplacement)
racine.mainloop()