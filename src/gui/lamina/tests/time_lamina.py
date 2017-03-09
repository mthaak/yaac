"""Timings for various subtasks of the lamina library. """

import sys

sys.path.insert(0, '..')

import timeit

import OpenGL.GL as ogl
import OpenGL.GLU as oglu
import pygame
from pygame.locals import *


def doNothing():
    pass


pygame.init()
screen = pygame.display.set_mode((400, 400), OPENGL)

txtr = surf = tD = None


def setup():
    global txtr, surf, tD
    txtr = ogl.glGenTextures(1)
    surf = pygame.Surface((1024, 1024), pygame.SRCALPHA, 32).convert_alpha()
    tD = pygame.image.tostring(surf, "RGBA", 1)


def trial_timertest():
    """test how timing is done. """
    pygame.time.delay(10)


def trial_tostring(surf):
    """time pygame's stringifier. """
    txtrData = pygame.image.tostring(surf, "RGBA", 1)


def trial_makeTexture(textureData):
    """ time texture object generator. """
    txtr = ogl.glGenTextures(1)
    ogl.glEnable(ogl.GL_TEXTURE_2D)
    ogl.glEnable(ogl.GL_BLEND)
    ogl.glBindTexture(ogl.GL_TEXTURE_2D, txtr)
    width, height = 1024, 1024
    ogl.glTexImage2D(ogl.GL_TEXTURE_2D, 0, ogl.GL_RGBA, width, height, 0,
                     ogl.GL_RGBA, ogl.GL_UNSIGNED_BYTE, textureData)
    ogl.glTexParameterf(ogl.GL_TEXTURE_2D, ogl.GL_TEXTURE_MAG_FILTER, ogl.GL_NEAREST)
    ogl.glTexParameterf(ogl.GL_TEXTURE_2D, ogl.GL_TEXTURE_MIN_FILTER, ogl.GL_NEAREST)
    ogl.glTexEnvf(ogl.GL_TEXTURE_ENV, ogl.GL_TEXTURE_ENV_MODE, ogl.GL_REPLACE)
    ogl.glBlendFunc(ogl.GL_SRC_ALPHA, ogl.GL_ONE_MINUS_SRC_ALPHA)
    ogl.glDisable(ogl.GL_BLEND)
    ogl.glDisable(ogl.GL_TEXTURE_2D)


gather = []


def trial_getpos(pos):
    """get 3d pos of window pos."""
    pos = oglu.gluUnProject(*pos)
    # gather.append(pos)


# ================

repct = 10
repct1 = 1000
setup()

r = timeit.Timer("trial_timertest()", "from __main__ import trial_timertest")
print
'timertest %8.3f' % (min(r.repeat(6, repct)) / repct)

r = timeit.Timer("trial_tostring(surf)", "from __main__ import trial_tostring, surf")
print
'tostring %8.3f' % (min(r.repeat(6, repct)) / repct)

r = timeit.Timer("trial_makeTexture(tD)", "from __main__ import trial_makeTexture, tD")
print
'makeTxtr %8.3f' % (min(r.repeat(6, repct)) / repct)

r = timeit.Timer("trial_getpos((0,0,0))", "from __main__ import trial_getpos")
print
'getpos 0,0,0 %8.6f' % (min(r.repeat(6, repct1)) / repct1)

r = timeit.Timer("trial_getpos((400,400,0))", "from __main__ import trial_getpos")
print
'getpos 400,400,0 %8.6f' % (min(r.repeat(6, repct1)) / repct1)
