#!/usr/bin/env python
# demo of laminar.PanelOverlaySurface, by
#  David Keeney 2006
# based on version of Nehe's OpenGL lesson04
#  by Paul Furber 2001 - m@verick.co.za

# you need pgu to be installed, and you need a copy of the default theme directory
#   as 'test_theme', and you need the accompanying config.txt in that test_theme dir.

import sys

sys.path.insert(0, '..')

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

# import gui stuff
# import gui stuff
try:
    from pgu import gui as pgui
except ImportError:
    print
    "PGU GUI must be installed in order to run this demo. "
    print
    "PGU can be obtained from: "
    print
    " https://sourceforge.net/project/showfiles.php?group_id=145281"
    sys.exit()

import lamina

rtri = rquad = 0.0

triOn = quadOn = True


def resize((width, height)):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0 * width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.5, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(-1.5, 0.0, -6.0)

    # draw triangle
    global rtri
    glRotatef(rtri, 0.0, 1.0, 0.0)

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, 0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(1.0, -1.0, 0)
    glEnd()

    # draw quad
    glLoadIdentity()
    glTranslatef(1.5, 0.0, -6.0)
    global rquad
    glRotatef(rquad, 1.0, 0.0, 0.0)

    glColor3f(0.5, 0.5, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(-1.0, 1.0, 0)
    glVertex3f(1.0, 1.0, 0)
    glVertex3f(1.0, -1.0, 0)
    glVertex3f(-1.0, -1.0, 0)
    glEnd()

    # draw gui
    glLoadIdentity()
    global gui_screen
    gui_screen.display()


def main():
    global rtri, rquad, gui_screen
    video_flags = OPENGL | DOUBLEBUF

    pygame.init()
    pygame.display.set_mode((640, 480), video_flags)
    font = pygame.font.SysFont("default", 18)
    fontBig = pygame.font.SysFont("default", 24)
    fontSub = pygame.font.SysFont("default", 20)
    theme = pgui.Theme('test_theme');

    resize((640, 480))
    init()

    # create PanelOverlaySurface
    #    gui_screen = lamina.LaminaPanelSurface((640,480), (-3.3, 2.5, 6.6, 5))
    gui_screen = lamina.LaminaScreenSurface()

    gui = pgui.App(theme=theme)
    gui._screen = gui_screen.surf

    # func to toggle triangle spin
    def triTog():
        global triOn
        triOn = not triOn

    # func to toggle quad spin
    def quadTog():
        global quadOn
        quadOn = not quadOn

    # create page    # layout using document
    lo = pgui.Container(width=640)

    # create page label
    title = pgui.Label("Lamina Demo : PGU", font=fontBig)
    lo.add(title, 29, 13)

    # create triangle button, connect to triTog handler function,
    #  and install in gui
    btn1 = pgui.Button("Stop/Start Triangle")
    btn1.connect(pgui.CLICK, triTog)
    lo.add(btn1, 120, 440)
    btn2 = pgui.Button("Stop/Start Quad")
    btn2.connect(pgui.CLICK, quadTog)
    lo.add(btn2, 420, 440)
    gui.init(lo)

    frames = 0
    ticks = pygame.time.get_ticks()
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        # handle gui events and raster updating
        gui.event((event))
        chg = gui.update(gui_screen.surf)
        if chg:
            gui_screen.refresh(chg)

        # draw all objects
        draw()

        # update rotation counters
        if triOn:
            rtri += 0.2
        if quadOn:
            rquad += 0.2

        # make changes visible
        pygame.display.flip()
        frames = frames + 1

    print
    "fps:  %d" % ((frames * 1000) / (pygame.time.get_ticks() - ticks))


if __name__ == '__main__': main()
