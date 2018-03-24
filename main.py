import copy
import os
import math
import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

vertices = []
reset_vertices = []
window = 0
width, height = 500, 500

C_ANIMATION = 20

def draw_2d():
    glBegin(GL_POLYGON)
    for x,y in vertices:
        glVertex2f(x, y)
    glEnd()

def draw_cartesian_lines():
    glBegin(GL_LINES)
    glVertex2f(0, -500)
    glVertex2f(0, 500)
    glVertex2f(-500, 0)
    glVertex2f(500, 0)
    glEnd()

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-500, 500, -500, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
    glLoadIdentity()                                   # reset position
    refresh2d(width, height)                           # set mode to 2d
    glLineWidth(2.5)
    glColor3f(255, 255, 255)
    draw_cartesian_lines()
    glColor3f(0.0, 0.0, 1.0)
    draw_2d()
    glutSwapBuffers()


def get_user_input():
    global vertices

    vertices = []

    print ('Masukan banyak titik = ',
    n = input())
    for i in range(1,n+1):
        print ('P({}) = '.format(i),
        x,y = input())
        vertices.append([x,y])
        reset_vertices.append([x,y])

def reset():
    global vertices
    vertices = copy.deepcopy(reset_vertices)
    draw()

def process_transformation_input(s):
    if s[0] == 'translate':
        translate(float(s[1]), float(s[2]))
    elif s[0] == 'reflect':
        reflect(s[1])
    elif s[0] == 'rotate':
        rotate(float(s[1]), int(s[2]), int(s[3]))
    elif s[0] == 'custom':
        custom(int(s[1]), int(s[2]), int(s[3]), int(s[4]))
    elif s[0] == 'dilate':
        dilate(float(s[1]))
    elif s[0] == 'shear':
        shear(s[1], float(s[2]))
    elif s[0] == 'stretch':
        stretch(s[1], float(s[2]))

def get_transformation_input():
    s = raw_input().split()

    if s[0] == 'multiple':
        multiple(int(s[1]))
    elif s[0] == 'exit':
        exit()
    elif s[0] == 'reset':
        reset()
    else:
        process_transformation_input(s)

    s = ''

# Melakukan translasi sebanyak dx dy
def translate(dx, dy):
    global vertices

    for c in range(C_ANIMATION):
        for i in range(len(vertices)):
            vertices[i][0] += dx/C_ANIMATION
            vertices[i][1] += dy/C_ANIMATION
        draw()

# Melakukan refleksi objek terhadap sumbu tertentu
def reflect(s):
    global vertices

    if s == 'x':
        for i in range(len(vertices)):
            vertices[i][0] *= -1
    elif s == 'y':
        for i in range(len(vertices)):
            vertices[i][1] *= -1
    elif s == 'y=x':
        for i in range(len(vertices)):
            vertices[i][0],vertices[i][1] = vertices[i][1],vertices[i][0]
    elif s == 'y=-x':
        for i in range(len(vertices)):
            vertices[i][0],vertices[i][1] = -1*vertices[i][1],-1*vertices[i][0]
    else:
        x = s[1:len(s)-1].split(',')
        if len(x) == 2:
            a,b = int(x[0]),int(x[1])
            for i in range(len(vertices)):
                vertices[i][0] = 2*a - vertices[i][0]
                vertices[i][1] = 2*b - vertices[i][1]
    draw()

# Rotasi objek
def rotate(deg, a, b):
    print ('rotate kepanggil')
    global vertices
    rad = math.radians(deg)
    for i in range(len(vertices)):
        tempx, tempy = vertices[i][0], vertices[i][1]
        vertices[i][0] = math.cos(rad)*(tempx-a) - math.sin(rad)*(tempy-b) + a
        vertices[i][1] = math.sin(rad)*(tempx-a) - math.cos(rad)*(tempy-b) + b
    draw()

# Perubahan objek dengan pengkalian matriks input
def custom(a, b, c, d):
    global vertices
    for i in range(len(vertices)):
        tempx = vertices[i][0]
        tempy = vertices[i][1]
        vertices[i][0] = a*tempx + b*tempy
        vertices[i][1] = c*tempx + d*tempy
    draw()

# Melakukan dilatasi terhadap objek
def dilate(k):
    global vertices
    for titik in vertices:
        titik[0] *= k
        titik[1] *= k
    draw()

# Penggeseran objek dengan p adalah sumbu yang dijadikan acuan, dan faktor pengali k
def shear (p, k) :
    global vertices
    if (p == 'x'):
        for titik in vertices :
            titik[0] += k * titik[1]
    elif (p == 'y'):
        for titik in vertices :
            titik[1] += k * titik[0]
    draw()

# Peregangan objek dengan p adalah sumbu yang dijadikan acuan, dan faktor pengali k
def stretch (p, k) :
    global vertices
    if (p == 'x'):
        for titik in vertices:
            titik[0] = k * titik[0]
    elif (p == 'y'):
        for titik in vertices:
            titik[1] = k * titik[1]
    draw()

# Melakukan transformasi linier sebanyak n kali secara berurutan
def multiple (n) :
    global vertices
    print('Melakukan transformasi linier pada objek sebanyak ', n, 'kali')
    for i in range (n) :
        s = raw_input('Transformasi ke-{}: '.format(i+1)).split()
        process_transformation_input(s)
    print('Pembacaan selesai')

# Keluar dari program
def exit():
    os._exit(0)

if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow(b"Tubes Algeo 2")
    glutDisplayFunc(draw)
    glutIdleFunc(get_transformation_input)
    get_user_input()
    glutMainLoop()
