import Terrain.py

def personnage(event):
    canvas.create_oval(RAPORT_CASE_C/3, RAPORT_CASE_R/3, 2*RAPORT_CASE_C/3, 2*RAPORT_CASE_R/3, fill="red")



canvas.bind('<Button-1>', personnage)