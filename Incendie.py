#########################################
# groupe DLBI
# Nabil HAMOUDI
# Essmay TOUANI
# Lauren EDOH COFFI
# Julie VALBERT
# Chloé GODET
# https://github.com/Nabil-hamoudi/Projet-Incendie-l1_UVSQ_lsin202
#########################################

########################
# import des librairies

import tkinter as tk

########################
# Constantes

COULEUR_FOND = "black"
BORDURE = "white"
LARGEUR = 1000
HAUTEUR = 800
NOMBRE_CASE_R = 8
NOMBRE_CASE_C = 8
RAPORT_CASE_R = HAUTEUR / NOMBRE_CASE_R
RAPORT_CASE_C = LARGEUR / NOMBRE_CASE_C

########################
# fonctions

def quadrillage():
    """Affiche un quadrillage sur le canvas."""
    global RAPORT_CASE_C, RAPORT_CASE_R

    for c in range(NOMBRE_CASE_C):
        taille_c = RAPORT_CASE_C * c
        canvas.create_line(taille_c, 0, taille_c, HAUTEUR, fill=BORDURE)

        for r in range(NOMBRE_CASE_R):
            taille_r = RAPORT_CASE_R * r
            canvas.create_line(0, taille_r, LARGEUR, taille_r, fill=BORDURE)


def start():
    """"""""
    pass


def changement():
    """"""
    pass

########################
# programme principal
racine = tk.Tk()
racine.title("Jeu de la vie")
# création des widgets
canvas = tk.Canvas(racine, bg=COULEUR_FOND, width=LARGEUR, height=HAUTEUR)
Start = tk.Button(
    racine, text="START", font=("helvetica", "20"), command=start)
quadrillage()
canvas.bind("<Button-1>", changement)
# placement des widgets
canvas.grid(row=1, columnspan=3)
Start.grid(row=0, column=1)
# boucle principale
racine.mainloop()
