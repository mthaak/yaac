#!/usr/bin/env python
# demo of laminar.PanelOverlaySurface, by
#  David Keeney 2006
# based on version of Nehe's OpenGL lesson04
#  by Paul Furber 2001 - m@verick.co.za

# you need the Ocemp GUI to be installed.

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

# import gui stuff
try:
    from ocempgui.widgets import *
    from ocempgui.widgets.components import TextListItem
    from ocempgui.widgets.Constants import *
except ImportError:
    print
    "OcempGUI version 0.1x must be installed in order to run this demo. "
    print
    " v0.2x will not work with Lamina. "
    print
    "Ocemp GUI 0.1x can be obtained from: "
    print
    " http://sourceforge.net/project/downloading.php?group_id=100329&filename=OcempGUI-0.1.3.tar.gz "
    sys.exit()

import sys

sys.path.insert(0, '..')

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

    resize((640, 480))
    init()

    # create PanelOverlaySurface
    #    gui_screen = lamina.LaminaPanelSurface((640,480), (-3.3, 2.5, 6.6, 5))
    gui_screen = lamina.LaminaScreenSurface()

    gui = Renderer()
    # the following is a workaround that may not be necessary
    #  by the time you read this.  We assign to the private attribute
    #  _screen to bypass drawing the background
    gui._screen = gui_screen.surf

    # if you are using a newer version of Ocemp GUI, use something like
    #  this instead.  The 0 alpha will make the background transparent.
    # gui.color = (0,0,0,0)
    # gui.screen = gui_screen.surf

    # func to toggle triangle spin
    def triTog():
        global triOn
        triOn = not triOn

    # func to toggle quad spin
    def quadTog():
        global quadOn
        quadOn = not quadOn

    # create page label
    lbl = Label('Lamina Demo : Ocemp')
    lbl.position = 29, 13
    gui.add_widget(lbl)
    # create triangle button, connect to triTog handler function,
    #  and install in gui
    btn1 = Button('Stop/Start Triangle')
    btn1.connect_signal(SIG_CLICKED, triTog)
    btn1.position = 120, 440
    gui.add_widget(btn1)
    # create quad button, connect to quadTog handler function,
    #  and install in gui    
    btn2 = Button('Stop/Start Quad')
    btn2.connect_signal(SIG_CLICKED, quadTog)
    btn2.position = 420, 440
    gui.add_widget(btn2)

    frames = 0
    ticks = pygame.time.get_ticks()
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        # handle gui events and raster updating
        gui.distribute_events((event))
        gui.update()
        dirty = gui.redraw(gui_screen.surf)
        if dirty:
            gui_screen.refresh(dirty)

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
