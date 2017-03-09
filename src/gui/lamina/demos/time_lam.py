#!/usr/bin/env python
# demo of laminar.PanelOverlaySurface, by
#  David Keeney 2006
# based on version of Nehe's OpenGL lesson04
#  by Paul Furber 2001 - m@verick.co.za

# you need the Ocemp GUI to be installed.

import sys

import pygame
from OpenGL.GL import *
from pygame.locals import *

sys.path.insert(0, '..')

import lamina
import timeit

gui_screen = None

rect_quarter = pygame.Rect(100, 100, 200, 200)
rect_half = pygame.Rect(59, 59, 282, 282)
rect_full = pygame.Rect(0, 0, 400, 400)
# rect_what = pygame.Rect(29,29,302,302)
rect_what = pygame.Rect(59, 59, 282, 282)


def setup():
    global gui_screen
    video_flags = OPENGL | DOUBLEBUF

    pygame.init()
    pygame.display.set_mode((400, 400), video_flags)

    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.5, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    # create PanelOverlaySurface
    gui_screen = lamina.LaminaScreenSurface()

    # draw text on a new Surface
    font = pygame.font.Font(None, 40)
    txt = font.render('Pygame Text', 1, (0, 0, 0), (200, 0, 0))
    gui_screen.surf.blit(txt, (75, 75))


def full():
    gui_screen.refresh()


def partial_quarter():
    gui_screen.refresh([rect_quarter])


def partial_half():
    gui_screen.refresh([rect_half])


def full2():
    gui_screen.refresh([rect_full])


def exp():
    gui_screen.refresh([rect_what])


# rfe = timeit.Timer("exp()", "from __main__ import exp, setup; setup()")
# print 'exp refresh %8.3f' % (rfe.timeit(100)/100)

rf = timeit.Timer("full()", "from __main__ import full, setup; setup()")
print
'full refresh %8.3f' % (rf.timeit(100) / 100)

rpq = timeit.Timer("partial_quarter()", "from __main__ import partial_quarter, setup; setup()")
print
'quarter refresh %8.3f' % (rpq.timeit(100) / 100)

rph = timeit.Timer("partial_half()", "from __main__ import partial_half, setup; setup()")
print
'half refresh %8.3f' % (rph.timeit(100) / 100)

rf2 = timeit.Timer("full2()", "from __main__ import full2, setup; setup()")
print
'full2 refresh %8.3f' % (rf2.timeit(100) / 100)
