# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import pygame
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import *
from pygame.constants import *

pygame.init()
viewport = (800, 600)
hx = viewport[0] / 2
hy = viewport[1] / 2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
# glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded

# LOAD OBJECT AFTER PYGAME INIT
arg = "road-tjunction-low.obj"
obj = OBJ(arg, swapyz=True)

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width / float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)

rx, ry = (0, 0)
tx, ty = (0, 0)
zpos = 5


def onPick(event):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)

    # RENDER OBJECT
    glTranslate(tx / 20., ty / 20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)

    glColor3f(0.3, 0.2, 0.4)
    glCallList(obj.gl_list)

    glTranslate(8, 8, 0)

    glColor3f(0.5, 0.3, 0.2)
    glCallList(obj.gl_list)

    x, y = event.pos[0], event.pos[1]
    color = glReadPixels(x, 600 - y, 1, 1, GL_RGB, GL_FLOAT)
    print(color)


rotate = move = False
i = 0
while 1:
    clock.tick(30)
    i = i + 150
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4:
                zpos = max(1, zpos - 1)
            elif e.button == 5:
                zpos += 1
            elif e.button == 1:
                onPick(e)
                rotate = True
            elif e.button == 3:
                move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1:
                rotate = False
            elif e.button == 3:
                move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glEnable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    glColor3f(1.0, 1.0, 1.0)

    # RENDER OBJECT
    glTranslate(tx / 20., ty / 20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)

    glCallList(obj.gl_list)

    glTranslate(8, 8, 0)

    glCallList(obj.gl_list)

    pygame.display.flip()
