from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import re
window = 0                                             # glut window number
width, height = 800, 600                               # window size
vertices = []
vertices_origin = []
awal = True
state = 0

def refresh2d(width, height):                           #intinya biar bisa 2D
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-500, 500, -500, 500, 0.0, 1.0)             #penyesuaian koordinat
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def polygon():
    global vertices                                     
    sumbu()
    glColor3f(0.0, 0.30, 0.0)                           #set warna objek
    glBegin(GL_POLYGON)
    for titik in vertices :
        glVertex2f(titik[0], titik[1])                  #menggambar polygon berdasarkan titik-titik
    glEnd()

def translate(dx, dy):  #maksudnya rekursif biar ada animasi, tapi ternyata enggak rapi animasinya
    global vertices
    global state

    if (dx >= 1 and dy >= 1):
        for titik in vertices :
            titik[0] += 1
            titik[1] += 1
        polygon()
        translate(dx-1, dy-1)
    elif (dx >= 1):
        for titik in vertices :
            titik[0] += 1
        polygon()
        translate(dx-1, dy)
    elif (dy >= 1):
        for titik in vertices :
            titik[1] += 1
        polygon()
        translate(dx, dy-1)
    elif (dx < 0 and dy < 0) :
        for titik in vertices :
            titik[0] -= 1
            titik[1] -= 1
        polygon()
        translate(dx+1, dy+1)
    elif (dx < 0):
        for titik in vertices :
            titik[0] -= 1
        polygon()
        translate(dx+1, dy)
    elif (dy < 0):
        for titik in vertices :
            titik[1] -= 1
        polygon()
        translate(dx, dy+1)
    else : #dx == 0 dan dy == 0
        polygon()
    glutSwapBuffers()

def dilate(k) : #dilasi objek dengan faktor pengali k
    global vertices
    for titik in vertices :
        titik[0] *= k
        titik[1] *= k
    polygon()

def shear (p, k) : #penggeseran objek dengan p adalah sumbu yang dijadikan acuan, dan faktor pengali k
    global vertices
    if (p == 'x') :
        for titik in vertices :
            titik[0] += k * titik[1]
    elif (p == 'y') :
        for titik in vertices :
            titik[1] += k * titik[0]
    polygon()

def stretch (p, k) : #peregangan objek dengan p adalah sumbu yang dijadikan acuan, dan faktor pengali k
    global vertices
    if (p == 'x') :
        for titik in vertices :
            titik[0] = k * titik[0]
    elif (p == 'y') :
        for titik in vertices :
            titik[1] = k * titik[1]
    polygon()

def multiple (n) :  #melakukan transformasi linier sebanyak n kali secara berurutan
    global vertices
    print('Melakukan transformasi linier pada objek sebanyak ', n, 'kali')
    for i in range (0, n) :
        param = [] #parameter-parameter yang digunakan dalam transformasi
        transformasi = input("Masukkan transformasi yang akan dilakukan : ")
        param = re.split(',| ',transformasi)
        if (param[0] == 'translate') :
            translate(int(param[1]), int(param[2]))
        elif(param[0] == 'dilate') :
            dilate(float(param[1]))
        elif(param[0] == 'shear') :
            shear(param[1], float(param[2]))
        elif(param[0] == 'stretch') :
            stretch(param[1], float(param[2]))
    print('Pembacaan selesai')
    polygon()
    
def sumbu():    #menggambar garis sumbu
    # Sumbu x
    glColor3f(1.0, 1.0, 1.0) 
    glBegin(GL_LINES)
    glVertex2f(-500,0)
    glVertex2f(500,0)
    glEnd()

    # Sumbu y
    glBegin(GL_LINES)
    glVertex2f(0,-500)
    glVertex2f(0,500)
    glEnd()


def draw():                                            # ondraw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
    glLoadIdentity()                                   # reset position
    refresh2d(width, height)                           # set mode to 2d 
    global state                                       # buat bedain pembacaan awal
    global vertices                                    #titik-titik yang membentuk objek, transformasi linier akan dilakukan pada titik-titik ini
    global vertices_origin                             #titik-titik asli sebelum dilakukan transformasi linier
    sumbu() #menggambar garis sumbu
    glColor3f(0.0, 0.30, 0.0)           
    
    if (state == 0) : #Membaca kondisi awal objek (membaca titik-titiknya)
        for i in range(n) :
            baca_titik = input("koordinat(x, y): ").split() #membaca input koordinat x dan y dipisahkan oleh spasi atau tanda koma
            baca_titik = [int(j) for j in baca_titik] #mengonversi ke integer
            vertices.append(baca_titik) #memasukkan pembacaan titik ke list
            polygon()
        state = 1
        vertices_origin = vertices #menyimpan bentuk semula objek di variabel lain (digunakan untuk reset)
        
    if (state == 1) : #objek terdefinisi, siap menerima input transformasi geometri yang hendak dilakukan
        polygon()
        glutSwapBuffers()   
        param = [] #parameter-parameter yang digunakan dalam transformasi
        transformasi = input("Masukkan transformasi yang akan dilakukan : ")
        param = re.split(',| ',transformasi) #parsing input yang diterima
        if (param[0] == 'translate') :
            translate(int(param[1]), int(param[2]))
        elif(param[0] == 'dilate') :
            dilate(float(param[1]))
        elif(param[0] == 'shear') :
            shear(param[1], float(param[2]))
        elif(param[0] == 'stretch') :
            stretch(param[1], float(param[2]))
        elif(param[0] == 'multiple') :
            multiple(int(param[1]))
    glutSwapBuffers()
    
                   
                       
# initialization
glutInit()                                             # initialize glut
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
# baca input n adalah jumlah titik
print("Masukkan banyaknya titik : ")
n = int(input())
#tampilkan objek yang dibentuk dari titik-titik tersebut
glutInitWindowSize(width, height)                      # set window size
glutInitWindowPosition(0, 0)                           # set window position
window = glutCreateWindow(b"Simulasi Transformasi Geometri")              # create window with title
glutDisplayFunc(draw)                                  # set draw function callback
glutIdleFunc(draw)                                     # draw all the time
glutMainLoop()                                         # start everything
