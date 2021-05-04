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

COULEUR_FOND = "black"
COULEUR = ["#006600", "#0000b3"]
# [0] terre, [1] eau
fullscreen = False
HAUTEUR = 600
LARGEUR = 800
NOMBRE_CASE = 50
RAPORT_CASE_R = HAUTEUR / NOMBRE_CASE
RAPORT_CASE_C = LARGEUR / NOMBRE_CASE
p = 0.5
n = 4
T = 5
K = 1
ValDefault = {
              "p": p, "n": n, "T": T, "K": K,
              "NOMBRE_CASE": NOMBRE_CASE,
              "HAUTEUR": HAUTEUR, "LARGEUR": LARGEUR,
              "fullscreen": fullscreen
              }

########################
# Variables globales

default = -1
# Contient le widget default
Chunk = [[], []]
# [1](0(gauche)/1(droite))
# [2](0->(nombre de chunk))
# [3](0->(Nombre Case C))
# [4](0->(Nombre case R))
# 0 => Terre , 1 => Eau
screen = [[]]

personnage = -1
# cercle rouge représentant le personnage
perso = False
# indique si le personnage existe
C_perso = -1
# colonne de la case du screen dans laquelle est placé le personnage
R_perso = -1
# ligne de la case du screen dans laquelle est placé le personnage
deplacements = []
# liste des déplacements effectués grâce aux flèches du clavier

Decalage = 0
tailleBlocage = 10

########################
# fonctions

########################
# Génération du terrain


def quadrillage(LR=1):
    """Génére un terrain de base, un terrain a droite ou un terrain a gauche"""
    # LR = 0,1 ou 3
    # 0 => gauche, 1 => Debut, 3 => Droite
    global Chunk, p
    LR = set([LR//2, LR % 2])
    for i in LR:
        Chunk[i].append(
                        [[-1 for i in range(NOMBRE_CASE)]for u in range(NOMBRE_CASE)]
                        )
        # Crée une Case de taille => (NOMBRE_CASE x NOMBRE_CASE)
        for C in range(NOMBRE_CASE):
            for R in range(NOMBRE_CASE):
                Ran = random.random()
                if Ran <= p:
                    Chunk[i][-1][C][R] = 1
                else:
                    Chunk[i][-1][C][R] = 0
    Correction(LR)


def Correction(LR):
    """Modifie les Case selon leur voisin"""
    global n, T, Chunk, NOMBRE_CASE
    for _ in range(n):
        for i in LR:
            TempChunk = []
            for C in range(NOMBRE_CASE):
                for R in range(NOMBRE_CASE):
                    count = Comptage(C, R, i, LR)
                    if count < T:
                        TempChunk.append([C, R, 0])
                    else:
                        TempChunk.append([C, R, 1])
            for r in TempChunk:
                Chunk[i][-1][r[0]][r[1]] = r[2]


def Comptage(C, R, i, LR):
    """Compte les valeurs des voisin (0 pour terre 1 pour eau)"""
    global NOMBRE_CASE, Chunk
    FinalCount = []
    count = CompteK(C, R)
    for n in count:
        # R_temp <= R_max and R_temp >= 0:
        if n[1] >= NOMBRE_CASE:
            if LR == {0, 1} and i == 0:
                FinalCount.append([i + 1, 0, n[0], n[1] - NOMBRE_CASE])
                # [i, chunk, C, R]
            elif LR != {0, 1}:
                FinalCount.append([i, -1, n[0], n[1] - NOMBRE_CASE])
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
    global NOMBRE_CASE, Chunk
    count = []
    C_max = NOMBRE_CASE - 1
    for o in [x for x in range(9) if x != 4]:
        C_temp = C - 1 + (o // 3)
        R_temp = R - 1 + (o % 3)
        if C_temp >= 0 and C_temp <= C_max:
            count.append([C_temp, R_temp])
    return count


####################################
# Déplacement du personage et création du terrain

def Decale(LR):
    """Decale la map sur la gauche ou la droite"""
    global Decalage, NOMBRE_CASE, tailleD
    global tailleG, tailleBlocage, C_perso, R_perso
    if LR == 0:
        Decalage -= 1
        Colored(LR)
    elif LR == 3:
        Decalage += 1
        Colored(LR)


def etat_terrain(C, R):
    """Retourne 0 si c'est une case de terre et 1 si c'est une case d'eau
    à partir de la colonne et de la ligne de la partie visible"""
    global Decalage
    P = 0
    R += Decalage
    if R < NOMBRE_CASE//2:
        R += NOMBRE_CASE//2
        while R < 0:
            P += 1
            R += NOMBRE_CASE
        while True:
            try:
                etat = Chunk[0][P][C][R]
                break
            except IndexError:
                quadrillage(0)
                etat = Chunk[0][P][C][R]
    else:
        R -= NOMBRE_CASE//2
        while R >= NOMBRE_CASE:
            P += 1
            R -= NOMBRE_CASE
        while True:
            try:
                etat = Chunk[1][P][C][R]
                break
            except IndexError:
                quadrillage(3)
                etat = Chunk[1][P][C][R]
    return etat


def Colored(LR=1):
    """Crée les cases vertes (terre) et bleues (eau)
    ou modifie les case existante"""
    global screen, RAPORT_CASE_C, RAPORT_CASE_R
    global NOMBRE_CASE, COULEUR
    if LR == 1:
        for C in range(NOMBRE_CASE):
            for R in range(NOMBRE_CASE):
                color = COULEUR[etat_terrain(C, R)]
                screen[C][R] = canvas.create_rectangle(
                                                       R*RAPORT_CASE_C,
                                                       C*RAPORT_CASE_R,
                                                       (R + 1) * RAPORT_CASE_C,
                                                       (C + 1) * RAPORT_CASE_R,
                                                       fill=color,
                                                       outline=color
                                                      )
    else:
        for C in range(NOMBRE_CASE):
            for R in range(NOMBRE_CASE):
                color = COULEUR[etat_terrain(C, R)]
                canvas.itemconfigure(
                                    screen[C][R],
                                    fill=color,
                                    outline=color
                                    )


def personnage(event):
    """Place le personnage sur la case cliquée
    et le retire si on clique sur la case dans laquelle il est déjà"""
    global personnage, perso, C_perso, R_perso, i_perso, deplacements
    if not perso:
        C_perso = int(event.x // RAPORT_CASE_C)
        R_perso = int(event.y // RAPORT_CASE_R)
        if etat_terrain(R_perso, C_perso) == 0:
            personnage = canvas.create_oval(
                                           C_perso*RAPORT_CASE_C+RAPORT_CASE_C/3,
                                           R_perso*RAPORT_CASE_R+RAPORT_CASE_R/3,
                                           C_perso*RAPORT_CASE_C+2*RAPORT_CASE_C/3,
                                           R_perso*RAPORT_CASE_R+2*RAPORT_CASE_R/3,
                                           fill="red"
                                           )
            perso = True
        else:
            tk.messagebox.showwarning(
                                      title="Attention !",
                                      message="Placez-vous sur une case de terre.",
                                      default="ok", icon="warning"
                                      )
    else:
        if event.x // RAPORT_CASE_C == C_perso and event.y // RAPORT_CASE_R == R_perso:
            canvas.delete(personnage)
            perso = False
            deplacements = []


def deplacement_haut(event):
    """Déplace le personnage d'une case
    vers le haut si on appuie sur la flèche vers le haut du clavier
    et enregistre le déplacement"""
    global personnage, perso, C_perso, R_perso
    if perso:
        if R_perso > 0:
            if etat_terrain(R_perso-1, C_perso) == 0:
                canvas.move(personnage, 0, -RAPORT_CASE_R)
                R_perso -= 1
                deplacements.append("h")


def deplacement_bas(event):
    """Déplace le personnage d'une case vers le bas
    si on appuie sur la flèche du bas du clavier
    et enregistre le déplacement"""
    global personnage, perso, C_perso, R_perso
    if perso:
        if R_perso < NOMBRE_CASE - 1:
            if etat_terrain(R_perso+1, C_perso) == 0:
                canvas.move(personnage, 0, RAPORT_CASE_R)
                R_perso += 1
                deplacements.append("b")


def deplacement_gauche(event):
    """Déplace le personnage d'une case vers la gauche
    si on appuie sur la flèche de gauche du clavier
    et enregistre le déplacement"""
    global personnage, perso, C_perso, R_perso, tailleBlocage
    if perso:
        if etat_terrain(R_perso, C_perso-1) == 0:
            if C_perso > NOMBRE_CASE // tailleBlocage:
                canvas.move(personnage, -RAPORT_CASE_C, 0)
                C_perso -= 1
                deplacements.append("g")
            else:
                Decale(0)
                deplacements.append("gE")


def deplacement_droite(event):
    """Déplace le personnage d'une case vers la droite
    si on appuie sur la flèche de droite du clavier
    et enregistre le déplacement"""
    global personnage, perso, C_perso, R_perso, tailleBlocage, NOMBRE_CASE
    if perso:
        if etat_terrain(R_perso, C_perso+1) == 0:
            if C_perso < (NOMBRE_CASE - 1)-(NOMBRE_CASE // tailleBlocage) and C_perso != (NOMBRE_CASE - 1):
                canvas.move(personnage, RAPORT_CASE_C, 0)
                C_perso += 1
                deplacements.append("d")
            else:
                Decale(3)
                deplacements.append("dE")


def annule_deplacement(event):
    """Annule le dernier déplacement effectué si on appuie sur Ctrl-z"""
    global deplacements, Decalage
    if len(deplacements) > 0:
        if deplacements[len(deplacements)-1] == "h":
            deplacement_bas(event)
            deplacements.pop()
            # suppression le déplacement ajouté par la fonction deplacement
        elif deplacements[len(deplacements)-1] == "b":
            deplacement_haut(event)
            deplacements.pop()
        elif deplacements[len(deplacements)-1] == "g":
            deplacement_droite(event)
            deplacements.pop()
        elif deplacements[len(deplacements)-1] == "d":
            deplacement_gauche(event)
            deplacements.pop()
        elif deplacements[len(deplacements)-1] == "dE":
            Decale(0)
        elif deplacements[len(deplacements)-1] == "gE":
            Decale(3)
        deplacements.pop()  # suppression du déplacement annulé


########################
# création des menus/paramétre


def jouer(evt):
    """Lance le jeu lorsque l'on appuie sur jouer"""
    global canvas, fen, RAPORT_CASE_C, RAPORT_CASE_R
    global screen, HAUTEUR, LARGEUR, fullscreen
    canvas.destroy()
    HAUTEUR = HAUTEUR
    LARGEUR = LARGEUR
    canvas = tk.Canvas(fen, width=LARGEUR, height=HAUTEUR, bg=COULEUR_FOND)
    canvas.grid()
    fen.attributes("-fullscreen", fullscreen)
    RAPORT_CASE_R = HAUTEUR / NOMBRE_CASE
    RAPORT_CASE_C = LARGEUR / NOMBRE_CASE
    screen = [[-1 for i in range(NOMBRE_CASE)]for u in range(NOMBRE_CASE)]
    quadrillage()
    Colored()
    Touchedirectionnel()


def Touchedirectionnel():
    """Bind les diférentes touches directionel pour le jeu"""
    canvas.bind('<Button-1>', personnage)
    canvas.bind_all("<Up>", deplacement_haut)
    canvas.bind_all("<Down>", deplacement_bas)
    canvas.bind_all("<Left>", deplacement_gauche)
    canvas.bind_all("<Right>", deplacement_droite)
    canvas.bind_all("<Control-KeyPress-z>", annule_deplacement)


def parametres(evt):
    """Ouvre la fenêtre des paramétres"""
    global default, NOMBRE_CASE, p, n, T, K, HAUTEUR, LARGEUR, fullscreen
    canvas.delete('all')

    canvas.create_text(
                       LARGEUR//2, HAUTEUR//5,
                       text="Paramètres", fill="white", font=('system', '45')
                       )
    canvas.create_text(
                       LARGEUR//2, 1.7*HAUTEUR//4,
                       text="Choix de la taille", fill="#3156E1",
                       activefill="white", font='Rockwell, 30', tags='taille'
                       )
    canvas.create_text(
                       LARGEUR//2, 2.3*HAUTEUR//4,
                       text="Choix des options", fill="#3156E1",
                       activefill="white", font="Rockwell, 28", tags='option'

                       )
    canvas.create_text(
                       LARGEUR//2, 2.9*HAUTEUR//4,
                       text="Choix de résolution", fill="#3156E1",
                       activefill="white",
                       font="Rockwell, 26", tags='reso'
                       )
    canvas.create_text(
                       LARGEUR//2, 7.2*HAUTEUR//8,
                       text="Valider", fill="white", activefill="green",
                       font="Rockwell, 25", tags='menu'
                       )
    if NOMBRE_CASE != ValDefault["NOMBRE_CASE"] or p != ValDefault["p"] or n != ValDefault["n"] or T != ValDefault["T"] or K != ValDefault["K"] or fullscreen != ValDefault["fullscreen"]:
        default = canvas.create_text(
                                     LARGEUR//2, 7.2*HAUTEUR//9,
                                     text="Défault", fill="white",
                                     activefill="green",
                                     font="Rockwell, 25", tags='default'
                                     )


def taille(evt):
    """Ouvre la fenêtre de modification de la taille en nombre de case"""
    global cursor_taille, NOMBRE_CASE
    canvas.delete('all')
    canvas.create_text(
                       LARGEUR//2, HAUTEUR//5,
                       text="Choix de la taille", fill="white",
                       font=('system', '45')
                       )
    canvas.create_text(
                       LARGEUR//2, 2*HAUTEUR//5,
                       text="Par défault la taille sera de 50x50 cases !",
                       fill="white", font=('system', '15')
                       )

    cursor_taille = tk.Scale(
                             canvas, orient='horizontal',
                             from_=2, to=100, tickinterval=98,
                             relief="groove", troughcolor="black",
                             font="system"
                             )
    cursor_taille.set(NOMBRE_CASE)
    cursor_taille.place(x=200, y=330, width=400)

    canvas.create_text(
                       LARGEUR//2, 4*HAUTEUR//5,
                       text="Valider", fill="white",
                       activefill="green", font="Rockwell, 25",
                       tags='valider_1'
                       )


def option(evt):
    """Ouvre la fenêtre des options
    dans laquelle on peut changer T, n, p et K"""
    global cursor_p, cursor_n, cursor_T
    global cursor_k, label_p, label_n, label_T, label_k
    global p, n, T, K
    canvas.delete('all')
    canvas.create_text(
                       LARGEUR//2, HAUTEUR//6,
                       text="Choix des options",
                       fill="white", font=('system', '45')
                       )

    cursor_p = tk.Scale(
                        canvas, from_=0, to=1,
                        resolution=0.1, tickinterval=1,
                        length=250, bg=COULEUR_FOND, fg="white"
                        )
    cursor_p.set(p)
    cursor_p.place(x=150, y=200)
    cursor_p.bind('<B1-Motion>', scale)
    label_p = tk.Label(
                       canvas, text="p = " + str(cursor_p.get()),
                       font="system", bg=COULEUR_FOND, fg="white"
                       )
    label_p.place(x=158, y=480)

    cursor_n = tk.Scale(
                        canvas, from_=0, to=10,
                        tickinterval=10, length=250,
                        bg=COULEUR_FOND, fg="white"
                        )
    cursor_n.set(n)
    cursor_n.place(x=300, y=200)
    cursor_n.bind('<B1-Motion>', scale2)
    label_n = tk.Label(
                       canvas, text="n = " + str(cursor_n.get()),
                       font="system", bg=COULEUR_FOND, fg="white"
                       )
    label_n.place(x=308, y=480)

    cursor_T = tk.Scale(
                        canvas, from_=0, to=100,
                        tickinterval=100, length=250,
                        bg=COULEUR_FOND, fg="white"
                        )
    cursor_T.set(T)
    cursor_T.place(x=450, y=200)
    cursor_T.bind('<B1-Motion>', scale3)
    label_T = tk.Label(
                       canvas,
                       text="T = " + str(cursor_T.get()),
                       font="system", bg=COULEUR_FOND, fg="white"
                       )
    label_T.place(x=458, y=480)

    cursor_k = tk.Scale(
                        canvas, from_=0, to=5,
                        tickinterval=5, length=250,
                        bg=COULEUR_FOND, fg="white"
                        )
    cursor_k.set(K)
    cursor_k.place(x=600, y=200)
    cursor_k.bind('<B1-Motion>', scale4)
    label_k = tk.Label(
                       canvas,
                       text="K = " + str(cursor_k.get()),
                       font="system", bg=COULEUR_FOND, fg="white"
                       )
    label_k.place(x=608, y=480)

    canvas.create_text(
                       LARGEUR//2, 7.2*HAUTEUR//8,
                       text="Valider", fill="white",
                       activefill="green", font="Rockwell, 25",
                       tags='valider_2'
                       )


def scale(evt):
    """affiche p ="""
    label_p.config(text="p = " + str(cursor_p.get()))


def scale2(evt):
    """affiche n ="""
    label_n.config(text="n = " + str(cursor_n.get()))


def scale3(evt):
    """affiche T ="""
    label_T.config(text="T = " + str(cursor_T.get()))


def scale4(evt):
    """affiche K ="""
    label_k.config(text="K = " + str(cursor_k.get()))


def resolution(evt):
    global FullScreenButton, fullscreen
    canvas.delete('all')
    canvas.create_text(
                       LARGEUR//2, HAUTEUR//5,
                       text="Choix de la résolution",
                       fill="white", font=('system', '40')
                       )

    canvas.create_text(
                       LARGEUR//2, 7.2*HAUTEUR//8,
                       text="Valider", fill="white",
                       activefill="green",
                       font="Rockwell, 25",
                       tags='valider_3'
                       )

    FullScreenButton = tk.Checkbutton(
                                      fen, text="FullScreen",
                                      font="Rockwell, 26",
                                      selectcolor="Black", bg="black",
                                      fg="white", command=ValideFullScreen
                                      )
    if fullscreen:
        FullScreenButton.select()
    FullScreenButton.place(x=300, y=400)


def ValideFullScreen():
    """Valide le FullScreen ou non"""
    global fullscreen, FullScreenButton
    if fullscreen:
        fullscreen = False
    else:
        fullscreen = True


def valider_reso(evt):
    """Valide la resolution selectionner"""
    global default, FullScreenButton, fullscreen
    FullScreenButton.destroy()
    canvas.delete('all')
    canvas.create_text(
                       LARGEUR//2, HAUTEUR//5,
                       text="Paramètres", fill="white", font=('system', '45')
                       )
    canvas.create_text(
                       LARGEUR//2, 1.7*HAUTEUR//4,
                       text="Choix de la taille", fill="#3156E1",
                       activefill="white", font='Rockwell, 30', tags='taille'
                       )
    canvas.create_text(
                       LARGEUR//2, 2.3*HAUTEUR//4,
                       text="Choix des options", fill="#3156E1",
                       activefill="white", font="Rockwell, 28", tags='option'

                       )
    canvas.create_text(
                       LARGEUR//2, 2.9*HAUTEUR//4,
                       text="Choix de résolution", fill="#3156E1",
                       activefill="white",
                       font="Rockwell, 26", tags='reso'
                       )
    if NOMBRE_CASE != ValDefault["NOMBRE_CASE"] or p != ValDefault["p"] or n != ValDefault["n"] or T != ValDefault["T"] or K != ValDefault["K"] or fullscreen != ValDefault["fullscreen"]:
        default = canvas.create_text(
                                     LARGEUR//2, 7.2*HAUTEUR//9,
                                     text="Défault", fill="white",
                                     activefill="green",
                                     font="Rockwell, 25", tags='default'
                                     )
    canvas.create_text(
                       LARGEUR//2, 7.2*HAUTEUR//8,
                       text="Valider", fill="white",
                       activefill="green", font="Rockwell, 25",
                       tags='menu'
                       )


def valider_taille(evt):
    """Valide les options de taille du jeu"""
    global taille, NOMBRE_CASE, HAUTEUR, default, ValDefault
    global LARGEUR, RAPORT_CASE_C, RAPORT_CASE_R, fullscreen
    taille = cursor_taille.get()
    NOMBRE_CASE = taille
    canvas.delete('all')
    cursor_taille.destroy()
    cursor_taille.destroy()
    canvas.create_text(
                       LARGEUR//2, HAUTEUR//5,
                       text="Paramètres", fill="white", font=('system', '45')
                       )
    canvas.create_text(
                       LARGEUR//2, 1.7*HAUTEUR//4,
                       text="Choix de la taille", fill="#3156E1",
                       activefill="white", font='Rockwell, 30', tags='taille'
                       )
    canvas.create_text(
                       LARGEUR//2, 2.3*HAUTEUR//4,
                       text="Choix des options", fill="#3156E1",
                       activefill="white", font="Rockwell, 28", tags='option'

                       )
    canvas.create_text(
                       LARGEUR//2, 2.9*HAUTEUR//4,
                       text="Choix de résolution", fill="#3156E1",
                       activefill="white",
                       font="Rockwell, 26", tags='reso'
                       )
    if NOMBRE_CASE != ValDefault["NOMBRE_CASE"] or p != ValDefault["p"] or n != ValDefault["n"] or T != ValDefault["T"] or K != ValDefault["K"] or fullscreen != ValDefault["fullscreen"]:
        default = canvas.create_text(
                                     LARGEUR//2, 7.2*HAUTEUR//9,
                                     text="Défault", fill="white",
                                     activefill="green",
                                     font="Rockwell, 25", tags='default'
                                     )
    canvas.create_text(
                       LARGEUR//2, 7.2*HAUTEUR//8,
                       text="Valider", fill="white",
                       activefill="green", font="Rockwell, 25",
                       tags='menu'
                       )


def valider_option(evt):
    """valide les paramétres p, n, T, k"""
    global p, n, T, K, default, ValDefault, fullscreen
    p = cursor_p.get()
    n = cursor_n.get()
    T = cursor_T.get()
    K = cursor_k.get()
    canvas.delete('all')
    cursor_p.destroy()
    cursor_n.destroy()
    cursor_T.destroy()
    cursor_k.destroy()
    label_p.destroy()
    label_n.destroy()
    label_T.destroy()
    label_k.destroy()
    canvas.create_text(
                       LARGEUR//2, HAUTEUR//5,
                       text="Paramètres", fill="white", font=('system', '45')
                       )
    canvas.create_text(
                       LARGEUR//2, 1.7*HAUTEUR//4,
                       text="Choix de la taille", fill="#3156E1",
                       activefill="white", font='Rockwell, 30', tags='taille'
                       )
    canvas.create_text(
                       LARGEUR//2, 2.3*HAUTEUR//4,
                       text="Choix des options", fill="#3156E1",
                       activefill="white", font="Rockwell, 28", tags='option'

                       )
    canvas.create_text(
                       LARGEUR//2, 2.9*HAUTEUR//4,
                       text="Choix de résolution", fill="#3156E1",
                       activefill="white",
                       font="Rockwell, 26", tags='reso'
                       )
    if NOMBRE_CASE != ValDefault["NOMBRE_CASE"] or p != ValDefault["p"] or n != ValDefault["n"] or T != ValDefault["T"] or K != ValDefault["K"] or fullscreen != ValDefault["fullscreen"]:
        default = canvas.create_text(
                                     LARGEUR//2, 7.2*HAUTEUR//9,
                                     text="Défault", fill="white",
                                     activefill="green",
                                     font="Rockwell, 25", tags='default'
                                     )
    canvas.create_text(
                       LARGEUR//2, 7.2*HAUTEUR//8,
                       text="Valider", fill="white",
                       activefill="green", font="Rockwell, 25",
                       tags='menu'
                       )


def default(evt):
    """Remet les options par défault"""
    global HAUTEUR, LARGEUR, NOMBRE_CASE, p, n, T, K, default, fullscreen
    canvas.delete("default")
    HAUTEUR = 600
    LARGEUR = 800
    p = 0.5
    n = 4
    T = 5
    K = 1
    NOMBRE_CASE = 50
    fullscreen = False


def main_menu(evt=None):
    """place les objets du menu"""
    canvas.delete('all')
    canvas.create_text(
                       LARGEUR//2, HAUTEUR//5,
                       text="MINECERAFT", fill="white",
                       font=('system', '40'), tags='sebastien'
                       )
    canvas.create_text(
                       LARGEUR//2, 2*HAUTEUR//5,
                       text="Jouer", fill="green",
                       activefill="white", font="Rockwell, 30",
                       tags='jouer'
                       )
    canvas.create_text(
                       LARGEUR//2, 3*HAUTEUR//5,
                       text="Paramètres", fill="white",
                       activefill="#3156E1", font="Rockwell, 25",
                       tags='para'
                       )
    canvas.create_text(
                       LARGEUR//2, 4*HAUTEUR//5,
                       text="Quitter", fill="red",
                       activefill="white", font="Rockwell, 30",
                       tags='quitter'
                       )


############################
# programme principal

fen = tk.Tk()

fen.title("Génération de terrain de jeu")
fen.config(bg=COULEUR_FOND)

canvas = tk.Canvas(fen, width=LARGEUR, height=HAUTEUR, bg=COULEUR_FOND)
canvas.grid()
main_menu()

canvas.tag_bind('jouer', '<Button-1>', jouer)
canvas.tag_bind('para', '<Button-1>', parametres)
canvas.tag_bind('quitter', '<Button-1>', lambda evt: fen.quit())
canvas.tag_bind('taille', '<Button-1>', taille)
canvas.tag_bind('option', '<Button-1>', option)
canvas.tag_bind('reso', '<Button-1>', resolution)
canvas.tag_bind('menu', '<Button-1>', main_menu)
canvas.tag_bind('default', '<Button-1>', default)
canvas.tag_bind('valider_1', '<Button-1>', valider_taille)
canvas.tag_bind('valider_2', '<Button-1>', valider_option)
canvas.tag_bind('valider_3', '<Button-1>', valider_reso)

fen.mainloop()
