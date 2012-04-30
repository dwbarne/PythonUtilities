from turtle import *

def carre(taille, couleur, angle):
    "fonction"
    color(couleur)
    c=0
    while c<4:
        left(angle)
        forward(taille)
        right(90)
        c = c+1

def triangle(taille, couleur, angle):
    "triangle"
    color(couleur)
    c=0
    while c<3:
        left(angle)
        forward(taille)
        right(120)
        c = c+1

#from dessins_tortue import *
up()
goto(-400,0)

n=0
while n < 5:
    down()                         # abaisser le crayon
#    carre(25*n, 'red', 0)            # tracer un carr?
    carre(25*n, 'red', 0)            # tracer un carr?
    up()
#    forward(30*n)
    forward(30*n)
    n=n+1
    triangle(90, 'blue',0)
    up()
    forward(115)
