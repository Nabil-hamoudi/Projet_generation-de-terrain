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

LARGEUR = 800
HAUTEUR = 600
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
# fonctions

def jouer(evt):
    canvas.delete('all')
    quadrillage()
    Colored()



def parametres(evt):
    canvas.delete('all')
    
    canvas.create_text(LARGEUR//2, HAUTEUR//5, text="Paramètres", fill="white", font=('system', '45'))
    canvas.create_text(LARGEUR//2, 2*HAUTEUR//4, text="Choix de la taille", fill="#3156E1", activefill="white", font='Rockwell, 30', tags='taille')
    canvas.create_text(LARGEUR//2, 2.7*HAUTEUR//4, text="Choix des options", fill="#3156E1", activefill="white", font="Rockwell, 30", tags='option')
    canvas.create_text(LARGEUR//2, 7.2*HAUTEUR//8, text="Valider", fill="white", activefill="green", font="Rockwell, 25", tags='menu')


def taille(evt):
    global cursor_taille
    canvas.delete('all')
    canvas.create_text(LARGEUR//2, HAUTEUR//5, text="Choix de la taille", fill="white", font=('system', '45'))
    canvas.create_text(LARGEUR//2, 2*HAUTEUR//5, text="Par défault la taille sera de 50x50 cases !", fill="white", font=('system', '15') )
    
    cursor_taille = tk.Scale(canvas, orient='horizontal', from_=2, to=100, tickinterval=98, relief="groove", troughcolor="black", font="system")
    cursor_taille.set(50)
    cursor_taille.place(x=200, y=330, width=400)

    canvas.create_text(LARGEUR//2, 4*HAUTEUR//5, text="Valider", fill="white", activefill="green", font="Rockwell, 25", tags='valider_1')


def option(evt):
    global cursor_p, cursor_n, cursor_T, cursor_k, label_p, label_n, label_T, label_k
    canvas.delete('all')
    canvas.create_text(LARGEUR//2, HAUTEUR//6, text="Choix des options", fill="white", font=('system', '45'))
    
    cursor_p = tk.Scale(canvas, from_=0, to=1, resolution=0.1, tickinterval=1, length=250, bg=COULEUR_FOND, fg="white")
    cursor_p.set(0.5)
    cursor_p.place(x=150, y=200)
    cursor_p.bind('<B1-Motion>', scale)
    label_p = tk.Label(canvas, text= "p = " + str(cursor_p.get()), font="system", bg=COULEUR_FOND, fg="white")
    label_p.place(x=158, y=480)

    cursor_n = tk.Scale(canvas, from_=0, to=10, tickinterval=10, length=250, bg=COULEUR_FOND, fg="white")
    cursor_n.set(4)
    cursor_n.place(x=300, y=200)
    cursor_n.bind('<B1-Motion>', scale2)
    label_n = tk.Label(canvas, text= "n = " + str(cursor_n.get()), font="system", bg=COULEUR_FOND, fg="white")
    label_n.place(x=308, y=480)

    cursor_T = tk.Scale(canvas, from_=0, to=100,tickinterval=100, length=250, bg=COULEUR_FOND, fg="white")
    cursor_T.set(5)
    cursor_T.place(x=450, y=200)
    cursor_T.bind('<B1-Motion>', scale3)
    label_T = tk.Label(canvas, text= "T = " + str(cursor_T.get()), font="system", bg=COULEUR_FOND, fg="white")
    label_T.place(x=458, y=480)

    cursor_k = tk.Scale(canvas, from_=0, to=5, tickinterval=5, length=250, bg=COULEUR_FOND, fg="white")
    cursor_k.set(1) 
    cursor_k.place(x=600, y=200)
    cursor_k.bind('<B1-Motion>', scale4)
    label_k = tk.Label(canvas, text= "k = " + str(cursor_k.get()), font="system", bg=COULEUR_FOND, fg="white")
    label_k.place(x=608, y=480)

    canvas.create_text(LARGEUR//2, 7.2*HAUTEUR//8, text="Valider", fill="white", activefill="green", font="Rockwell, 25", tags='valider_2')



def scale(evt):
    label_p.config(text= "p = " + str(cursor_p.get()))

def scale2(evt):
    label_n.config(text= "n = " + str(cursor_n.get()))

def scale3(evt):
    label_T.config(text= "T = " + str(cursor_T.get()))

def scale4(evt):
    label_k.config(text= "k = " + str(cursor_k.get()))


def valider_taille(evt):
    global taille
    taille = cursor_taille.get()
    print(taille)
    canvas.delete('all')
    cursor_taille.destroy()
    cursor_taille.destroy()
    canvas.create_text(LARGEUR//2, HAUTEUR//5, text="Paramètres", fill="white", font=('system', '45'))
    canvas.create_text(LARGEUR//2, 2*HAUTEUR//4, text="Choix de la taille", fill="#3156E1", activefill="white", font='Rockwell, 30', tags='taille')
    canvas.create_text(LARGEUR//2, 2.7*HAUTEUR//4, text="Choix des options", fill="#3156E1", activefill="white", font="Rockwell, 30", tags='option')
    canvas.create_text(LARGEUR//2, 7.2*HAUTEUR//8, text="Valider", fill="white", activefill="green", font="Rockwell, 25", tags='menu')


def valider_option(evt):
    global p, n, T, k
    p = cursor_p.get()
    n = cursor_n.get()
    T = cursor_T.get()
    k = cursor_k.get()
    print(p, n, T, k)
    canvas.delete('all')
    cursor_p.destroy()
    cursor_n.destroy()
    cursor_T.destroy()
    cursor_k.destroy()
    label_p.destroy()
    label_n.destroy()
    label_T.destroy()
    label_k.destroy()
    canvas.create_text(LARGEUR//2, HAUTEUR//5, text="Paramètres", fill="white", font=('system', '45'))
    canvas.create_text(LARGEUR//2, 2*HAUTEUR//4, text="Choix de la taille", fill="#3156E1", activefill="white", font='Rockwell, 30', tags='taille')
    canvas.create_text(LARGEUR//2, 2.7*HAUTEUR//4, text="Choix des options", fill="#3156E1", activefill="white", font="Rockwell, 30", tags='option')
    canvas.create_text(LARGEUR//2, 7.2*HAUTEUR//8, text="Valider", fill="white", activefill="green", font="Rockwell, 25", tags='menu')


def main_menu(evt=None):
    canvas.delete('all')
    canvas.create_text(LARGEUR//2, HAUTEUR//5, text="MINECERAFT", fill="white", font=('system', '40'), tags='sebastien')
    canvas.create_text(LARGEUR//2, 2*HAUTEUR//5, text="Jouer", fill="green", activefill="white", font="Rockwell, 30", tags='jouer')
    canvas.create_text(LARGEUR//2, 3*HAUTEUR//5, text="Paramètres", fill="white", activefill="#3156E1", font="Rockwell, 25", tags='para')
    canvas.create_text(LARGEUR//2, 4*HAUTEUR//5, text="Quitter", fill="red", activefill="white", font="Rockwell, 30", tags='quitter')


# programme principal
def main():
    global fen, canvas
    fen = tk.Tk()
    fen.maxsize(LARGEUR, HAUTEUR)
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
    canvas.tag_bind('menu', '<Button-1>', main_menu)
    canvas.tag_bind('valider_1', '<Button-1>', valider_taille)
    canvas.tag_bind('valider_2', '<Button-1>', valider_option)
    
    fen.mainloop()

main()


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

# placement des widgets
canvas.grid(row=1, columnspan=3)
# boucle principale
racine.mainloop()
