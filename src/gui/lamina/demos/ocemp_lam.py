#!/usr/bin/env python
# demo of laminar.PanelOverlaySurface, by
#  David Keeney 2006
#
# see http://pitchersduel.iuplog.com/default.asp?item=170661
#
# this demo requires pygame, pyopengl, Ocemp GUI and Spyre libraries,
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
        global gui, gui_screen
        if ev.type == pygame.QUIT:
            raise spyre.EngineShutdownException
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            raise spyre.EngineShutdownException
        # pass event to gui
        else:
            gui.distribute_events((ev))
            gui.update()
            chg = gui.redraw(gui_screen.surf)
            if len(chg):
                # gui_screen.regen()
                # gui_screen.clear()
                gui_screen.refresh(chg)
            self.engine.redisplay()


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

screenSize = (642, 429)


# define the necessary callback functions.
#  these are connected to signals within their respective
#  widgets, and invoked by the gui
#
def logAction(ed, text):
    """ add the text to the 'edit' window (callback function)"""
    ed.items.append(TextListItem(text))


def logButtonAction(ed, btn, text):
    """ add the button status to the 'edit' window (callback function)"""
    if btn.active:
        text += ' selected'
    else:
        text += ' deselected'
    # text += str(btn.active)
    ed.items.append(TextListItem(text))


def logTextAction(ed, txtWidget):
    """ add the text to the 'edit' window (callback function)"""
    text = txtWidget.text
    ed.items.append(TextListItem(text))


def logSlider(ev, ed, slider):
    """ add the slider position to the 'edit' window (callback function)"""
    # text = str(slider.get_coords_from_value())
    text = 'Slider is at ' + str(int(slider.value)) + ' %'
    ed.items.append(TextListItem(text))


def logImageMap(ev, ed, orig):
    """Add the click position to the 'edit' window (callback function)"""
    text = 'ImageMap click at %i, %i' % (ev.pos[0] - orig[0], ev.pos[1] - orig[1])
    ed.items.append(TextListItem(text))


def progBar(pb, list):
    """ update progress bar for len of list (callback function)"""
    prog = len(list) / 20.0 * 100
    if prog > 100: prog = 100
    pb.set_value(prog)


# create the gui, buttons and all, here
#
def make_gui(screen):
    """this function is called when the program starts.
    it initializes everything it needs, then runs in
    a loop until the function returns.
    """

    # screen = lamina.MonitorSurface(rawscreen)
    # create GUI object
    gui = Renderer()
    gui._screen = screen

    # create page label
    lbl = Label('Pygame GUI Test Page - Ocemp')
    lbl.position = 29, 13
    gui.add_widget(lbl)

    # create progress bar label
    lbl4 = Label('Progress Bar')
    lbl4.position = 356, 355
    gui.add_widget(lbl4)
    # progress bar
    pb = ProgressBar()
    pb.position = 354, 376
    gui.add_widget(pb)

    # create edit box
    ed = ScrolledList(250, 320)
    ed.scrolling = SCROLL_ALWAYS
    ed.items.append(TextListItem('top line of input'))
    ed.items.append(TextListItem('second line of input'))
    ed.position = 367, 19
    gui.add_widget(ed)
    progBar(pb, ed.items)  # update progress bar for above two items
    ed.connect_signal(SIG_LISTCHANGED, progBar, pb, ed.items)

    # create checkbuttons and add to gui
    cb1 = CheckButton('Check Box #1')
    cb1.position = 52, 40
    cb1.connect_signal(SIG_CLICKED, logButtonAction, ed, cb1, 'Check Box #1 clicked')
    gui.add_widget(cb1)
    cb2 = CheckButton('Check Box #2')
    cb2.position = 52, 70
    cb2.connect_signal(SIG_CLICKED, logButtonAction, ed, cb2, 'Check Box #2 clicked')
    gui.add_widget(cb2)
    cb3 = CheckButton('Check Box #3')
    cb3.position = 52, 98
    cb3.connect_signal(SIG_CLICKED, logButtonAction, ed, cb3, 'Check Box #3 clicked')
    gui.add_widget(cb3)

    # create radio buttons, put in table, and add to gui
    rbTab = Table(3, 1)
    rbTab.position = 210, 40
    rb1 = RadioButton('Radio Button #1', None)
    rb1.connect_signal(SIG_TOGGLED, logButtonAction, ed, rb1, 'Radio Button #1 ')
    rbTab.add_child(0, 0, rb1)
    rb2 = RadioButton('Radio Button #2', rb1)
    rb2.connect_signal(SIG_TOGGLED, logButtonAction, ed, rb2, 'Radio Button #2 ')
    rbTab.add_child(1, 0, rb2)
    rb3 = RadioButton('Radio Button #3', rb1)
    rb3.connect_signal(SIG_TOGGLED, logButtonAction, ed, rb3, 'Radio Button #3 ')
    rbTab.add_child(2, 0, rb3)
    gui.add_widget(rbTab)

    # create txt box label
    lbl2 = Label('Text Box')
    lbl2.position = 31, 130
    gui.add_widget(lbl2)
    # create text box
    en = Entry()
    en.position = 31, 155
    en.size = 250, 21
    en.connect_signal(SIG_INPUT, logTextAction, ed, en)
    gui.add_widget(en)

    # create slider label
    lbl3 = Label('Slider')
    lbl3.position = 31, 190
    gui.add_widget(lbl3)
    # create slider
    sl = HScale(0, 100, 1)
    sl.position = 31, 215
    sl.size = 200, 20
    sl.connect_signal(SIG_MOUSEUP, logSlider, ed, sl)
    gui.add_widget(sl)

    # add buttons, both regular and toggle
    btnTab = Table(2, 3)
    btnTab.position = 30, 250
    btnTab.spacing = 10
    btn1 = Button('Button 1')
    btn1.connect_signal(SIG_CLICKED, logAction, ed, 'Button 1 clicked')
    btnTab.add_child(0, 0, btn1)
    btn2 = Button('Button 2')
    btn2.connect_signal(SIG_CLICKED, logAction, ed, 'Button 2 clicked')
    btnTab.add_child(0, 1, btn2)
    btn3 = Button('Button 3')
    btn3.connect_signal(SIG_CLICKED, logAction, ed, 'Button 3 clicked')
    btnTab.add_child(0, 2, btn3)

    btnA = ToggleButton('Button A')
    btnA.connect_signal(SIG_TOGGLED, logButtonAction, ed, btnA, 'Button A ')
    btnTab.add_child(1, 0, btnA)
    btnB = ToggleButton('Button B')
    btnB.connect_signal(SIG_TOGGLED, logButtonAction, ed, btnB, 'Button B ')
    btnTab.add_child(1, 1, btnB)
    btnC = ToggleButton('Button C')
    btnC.connect_signal(SIG_TOGGLED, logButtonAction, ed, btnC, 'Button C ')
    btnTab.add_child(1, 2, btnC)
    gui.add_widget(btnTab)

    # create image map
    imap = ImageMap("clear.png")
    imap_pos = (31, 340)
    imap.connect_signal(SIG_MOUSEUP, logImageMap, ed, imap_pos)
    imap.position = imap_pos
    gui.add_widget(imap)

    # make some insensitive
    btn2.sensitive = False
    cb3.sensitive = False

    return gui


# Initialize Everything
pygame.init()
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
gui = make_gui(gui_screen.surf)

# put gui 
gui.update()
gui.redraw(gui_screen.surf)
gui_screen.refresh()

# run engine
engine.go()
