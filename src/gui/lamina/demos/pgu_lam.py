#!/usr/bin/env python
# demo of laminar.PanelOverlaySurface, by
#  David Keeney 2006, 2007
#
# this demo requires pygame, pyopengl, PGU GUI and Spyre libraries,
#  they should be available from the cheeseshop.python.org repository

import sys

sys.path.insert(0, '..')

import pygame
import OpenGL.GLU as oglu
import OpenGL.GL as ogl
import time

import spyre


class GUIInterface(spyre.BasicInterface):
    def event(self, ev):
        """Handle all interface events (from Pygame events)
        @param ev: pygame event 
        """
        global gui, gui_screen, lines
        if ev.type == pygame.QUIT:
            raise spyre.EngineShutdownException
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            raise spyre.EngineShutdownException
        # pass event to gui
        else:
            # pass event to gui
            gui.event(ev)
            chg = gui.update(gui_screen.surf)
            while len(lines) > lineLimit:
                lines[0:1] = []
            edText = "\n".join(lines)
            progBar(pb, lines)
            text.writepre(gui_screen.surf, font, textArea, (128, 128, 128), edText)
            if len(chg):
                gui_screen.refresh()  # markup output changes not in chg list


class YZPanel(spyre.Group):
    """Panel to display 2D stuff in 3D space. """

    def __init__(self):
        spyre.Group.__init__(self)

    def display(self):
        """Setup panel, and display group elements. """
        ogl.glPushMatrix()
        ogl.glRotate(90, 0, 1, 0)
        spyre.Group.display(self)
        ogl.glPopMatrix()


class Sphere(spyre.Object):
    def display(self):
        ogl.glPushMatrix()
        ogl.glTranslate(-1, -3.3, 1)
        ang = ((time.time() / 40) % 1) * 360  # 2*3.14
        ogl.glRotate(ang, 0, 0, 1)
        quad = oglu.gluNewQuadric()
        oglu.gluQuadricDrawStyle(quad, oglu.GLU_LINE)
        oglu.gluSphere(quad, 0.7, 15, 15)
        ogl.glPopMatrix()


import lamina

# import gui stuff
try:
    from pgu import text, gui as pgui
except ImportError:
    print
    "PGU GUI must be installed in order to run this demo. "
    print
    "PGU can be obtained from: "
    print
    " https://sourceforge.net/project/showfiles.php?group_id=145281"
    sys.exit()

screenSize = (642, 429)
lines = []
lineLimit = 20


def logRadioAction(arg):
    """ add the radio button status to the 'edit' window (callback function)"""
    grp, text = arg
    text = "Radio Button " + str(grp.value) + " selected"
    lines.append(text)
    while len(lines) > lineLimit: lines[0:1] = []


def logCheckAction(arg):
    """ add the button status to the 'edit' window (callback function)"""
    btn, text = arg
    if btn.value:
        text += ' selected';
    else:
        text += ' deselected';
    lines.append(text)


def logImg(_event, _widget, _code):
    """logImg """
    posstr = 'Image Map ' + str(_event.pos)
    lines.append(posstr)


def logButtonAction(text):
    """ add the button status to the 'edit' window (callback function)"""
    lines.append(text)
    while len(lines) > lineLimit: lines[0:1] = []


def logInputAction(txt):
    """ add the input status to the 'edit' window (callback function)"""
    text = txt.value
    lines.append(text)
    while len(lines) > lineLimit: lines[0:1] = []


def logSliderAction(txt):
    """ add the slider status to the 'edit' window (callback function)"""
    text = 'Slider is at ' + str(txt.value)
    lines.append(text)
    while len(lines) > lineLimit: lines[0:1] = []


def progBar(pb, list):
    """ update progress bar for len of list (callback function)"""
    prog = len(list) / 20.0 * 100
    if prog > 100: prog = 100
    pb.value = prog


pb, font, textArea, lines = None, None, None, None


def make_gui():
    global pb, font, textArea, lines

    font = pygame.font.SysFont("default", 18)
    fontBig = pygame.font.SysFont("default", 24)
    fontSub = pygame.font.SysFont("default", 20)
    theme = pgui.Theme('test_theme');

    # create GUI object
    gui = pgui.App(theme=theme)
    textArea = pygame.Rect(390, 20, 250, 320)

    # layout using document
    lo = pgui.Container(width=screenSize[0])

    # create page label
    # lo.block(align=-1) #lo.br(8) #lo.tr()
    title = pgui.Label("Pygame GUI Test Page - PGU", font=fontBig)
    lo.add(title, 29, 13)

    # create progress bar label
    # progress bar
    pbl = pgui.Label('Progress Bar')
    lo.add(pbl, 354, 351)
    pb = pgui.ProgressBar(10, 0, 100, width=200)
    lo.add(pb, 354, 371)

    # create checkbuttons and add to gui
    cbt = pgui.Table()
    cb1 = pgui.Switch()
    cb1.connect(pgui.CHANGE, logCheckAction, (cb1, "Check Box 1"))
    cb1l = pgui.Label("Check Box 1")
    cbt.add(cb1)
    cbt.add(cb1l)
    cbt.tr()
    cb2 = pgui.Switch()
    cb2.connect(pgui.CHANGE, logCheckAction, (cb2, "Check Box 2"))
    cb2l = pgui.Label("Check Box 2")
    cbt.add(cb2)
    cbt.add(cb2l)
    cbt.tr()
    cb3 = pgui.Switch()
    cb3.connect(pgui.CHANGE, logCheckAction, (cb3, "Check Box 3"))
    cb3l = pgui.Label("Check Box 3")
    cbt.add(cb3)
    cbt.add(cb3l)
    lo.add(cbt, 52, 52)

    # create radio buttons, put in table, and add to gui
    rbt = pgui.Table()
    radio = pgui.Group()
    rb1 = pgui.Radio(radio, 1)
    rb1l = pgui.Label("Radio Button 1")
    rbt.add(rb1)
    rbt.add(rb1l)
    rbt.tr()
    rb2 = pgui.Radio(radio, 2)
    rb2l = pgui.Label("Radio Button 2")
    rbt.add(rb2)
    rbt.add(rb2l)
    rbt.tr()
    rb3 = pgui.Radio(radio, 3)
    rb3l = pgui.Label("Radio Button 3")
    rbt.add(rb3)
    rbt.add(rb3l)
    rbt.tr()
    lo.add(rbt, 210, 52)
    radio.connect(pgui.CHANGE, logRadioAction, (radio, "Radio Button 3"))

    # create txt box label
    txtl = pgui.Label("Text Box", font=fontSub)
    lo.add(txtl, 30, 127)
    # create text box
    txt = pgui.Input("next line of input", size=40)
    txt.connect(pgui.BLUR, logInputAction, txt)
    lo.add(txt, 28, 149)

    # add buttons, both regular and toggle
    btn1 = pgui.Button("Button 1")
    btn1.connect(pgui.CLICK, logButtonAction, ("Button 1 clicked"))
    lo.add(btn1, 36, 250)
    btn2 = pgui.Button("Button 2")
    btn2.connect(pgui.CLICK, logButtonAction, ("Button 2 clicked"))
    lo.add(btn2, 133, 250)
    btn3 = pgui.Button("Button 3")
    btn3.connect(pgui.CLICK, logButtonAction, ("Button 3 clicked"))
    lo.add(btn3, 230, 250)

    # create toggle button not avail label
    tbl = pgui.Label("Toggle Buttons Not Supported")
    lo.add(tbl, 36, 290)

    img = pgui.Image("clear.png")
    img.connect(pgui.CLICK, logImg)
    # iml = pgui.Label("Image Map Not Supported")
    lo.add(img, 36, 340)

    # create slider label
    sll = pgui.Label("Slider", font=fontSub)
    lo.add(sll, 36, 195)
    # create slider
    sl = pgui.HSlider(value=1, min=0, max=100, size=32, width=200, height=16)
    sl.connect(pgui.CHANGE, logSliderAction, sl)
    lo.add(sl, 53, 210)  # , colspan=3)

    # make some insensitive
    btn2.disabled = True
    cb3.disabled = True

    # clear setup noise, and put initial content in
    lines = []
    lines.append('top line of input')
    lines.append('second line of input')
    progBar(pb, lines)  # update progress bar for above two items

    gui.init(lo)

    return gui


# Initialize Everything
pygame.init()
pygame.font.init()

engine = spyre.Engine()
engine.width, engine.height = screenSize
engine.interface = GUIInterface(engine)
engine.camera = spyre.BasicCameraOrtho(engine, (1, 0, 0))
engine.init()

# create objects and add to engine
sph = Sphere()
engine.add(sph)

# create lights
engine.studio = spyre.StudioColorMat(engine)
light0 = spyre.Bulb([0.8, 0.8, 0.8, 1.0],  # ambient
                    [0.8, 0.7, 0.7, 1.0],  # diffuse
                    [0.3, 0.3, 0.3, 1.0], )  # specular
engine.studio.addFixedLight(light0, (0, 5, 10))

# create alternate screen for gui
gui_screen = lamina.LaminaPanelSurface((-5, 5, 10, 10), screenSize)
pnl = YZPanel()
pnl.append(gui_screen)

engine.add(pnl)
gui = make_gui()

# put gui on screen
gui.paint(gui_screen.surf)
gui_screen.refresh()

# run engine
engine.go()
