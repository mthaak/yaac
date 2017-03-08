import sys

import pygame
from pygame.constants import *
from pygame.key import *

from src.gui.Renderer import Renderer


def start_pygame():
    import os
    import sys
    import warnings
    from optparse import OptionParser

    # from .game import PGZeroGame, DISPLAY_FLAGS
    # from . import loaders
    # from . import builtins

    def _check_python_ok_for_pygame():
        """If we're on a Mac, is this a full Framework python?

        There is a problem with PyGame on Macs running in a virtual env.
        If the Python used is from the venv, it will not allow full window and
        keyboard interaction. Instead, we need the original framework Python
        to get PyGame working properly.

        The problem doesn't occur on Linux and Windows.
        """
        if sys.platform == 'darwin':  # This is a Mac
            return 'Library/Frameworks' in sys.executable
        else:
            return True

    def _substitute_full_framework_python():
        """Need to change the OS/X Python executable to the full Mac version,
        while maintaining the virtualenv environment, so things still run
        in an encapsulated way.

        We do this by extract the paths that virtualenv has added to the system
        path, and prefixing them to the current PYTHONPATH.

        Then we use os.execv() to start a replacement process that uses the
        same environment as the previous one.
        """
        PYVER = '3.4'
        base_fw = '/Library/Frameworks/Python.framework/Versions/'
        framework_python = base_fw + '{pv}/bin/python{pv}'.format(pv=PYVER)
        venv_base = os.environ.get('VIRTUAL_ENV')
        if not venv_base:
            # Do nothing if virtual env hasn't been set up
            return
        venv_paths = [p for p in sys.path if p.startswith(venv_base)]
        # Need to allow for PYTHONPATH not already existing in environment
        os.environ['PYTHONPATH'] = ':'.join(venv_paths + [
            os.environ.get('PYTHONPATH', '')]).rstrip(':')
        # Pass command line args to the new process
        os.execv(framework_python, ['python', '-m', 'pgzero'] + sys.argv[1:])

    def main():

        # Pygame won't run from a normal virtualenv copy of Python on a Mac
        if not _check_python_ok_for_pygame():
            _substitute_full_framework_python()

        parser = OptionParser()
        options, args = parser.parse_args()

        if len(args) != 1:
            parser.error("You must specify which module to run.")

        if __debug__:
            warnings.simplefilter('default', DeprecationWarning)

        path = args[0]
        with open(path) as f:
            src = f.read()

        code = compile(src, os.path.basename(path), 'exec', dont_inherit=True)

        # loaders.set_root(path)

        pygame.display.set_mode((100, 100), DISPLAY_FLAGS)
        # name, _ = os.path.splitext(os.path.basename(path))
        # mod = ModuleType(name)
        # mod.__file__ = path
        # mod.__name__ = name
        # mod.__dict__.update(builtins.__dict__)
        # sys.modules[name] = mod
        # exec(code, mod.__dict__)
        # PGZeroGame(mod).run()


class GUI:
    def __init__(self, map, alg):
        self.map = map
        self.alg = alg

        # Set up Pygame
        start_pygame()
        # pygame.init()
        self.screen_width, self.screen_height = 1080, 720
        viewport = (self.screen_width, self.screen_height)
        hx = viewport[0] / 2
        hy = viewport[1] / 2
        srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
        pygame.display.set_caption('YAAC')
        self.clock = pygame.time.Clock()

        # Set up renderer
        self.renderer = Renderer(map)

        # Set view
        self.renderer._setView(viewport)

        # Set view parameters
        self.show_grid = False  # whether grid should be shown
        self.show_edges = True  # whether edges should be shown
        self.phi, self.theta = 90, 350
        self.zpos = 15
        self.renderer.setOrbit(self.phi, self.theta)
        self.renderer.setZoom(self.zpos)

        self.select = None

        self.alg.update()  # first update needed to get good orientation

        self.mainloop()  # start main loop

    def mainloop(self):
        while 1:
            self.clock.tick(3000)  # fix fps on 30 fps

            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()
                elif e.type == KEYDOWN and e.key == K_ESCAPE:
                    sys.exit()
                elif e.type == KEYDOWN and e.key == K_g:
                    self.show_grid = not self.show_grid
                elif e.type == KEYDOWN and e.key == K_e:
                    self.show_edges = not self.show_edges
                elif e.type == MOUSEBUTTONDOWN:
                    if e.button == 4:
                        self.zpos = max(9, self.zpos - 1)
                        self.renderer.setZoom(self.zpos)
                    elif e.button == 5:
                        self.zpos = min(50, self.zpos + 1)
                        self.renderer.setZoom(self.zpos)
                    elif e.button == 1:
                        self.select = self.renderer.getTileCoords(e.pos[0], e.pos[1], self.screen_height)
                        if self.select is not None:
                            self.map.toggleTile(*self.select)

            if get_pressed()[K_LEFT]:
                self.phi -= 5
                self.renderer.setOrbit(self.phi, self.theta)
            if get_pressed()[K_RIGHT]:
                self.phi += 5
                self.renderer.setOrbit(self.phi, self.theta)
            if get_pressed()[K_DOWN] and self.theta >= 280 + 5:
                self.theta -= 5
                self.renderer.setOrbit(self.phi, self.theta)
            if get_pressed()[K_UP] and self.theta <= 350 - 5:
                self.theta += 5
                self.renderer.setOrbit(self.phi, self.theta)

            # Render
            edges = self.alg.edges if self.show_edges else {}
            self.renderer.renderMap(select=self.select, show_grid=self.show_grid, edges=edges)
            move_done = self.renderer.renderEntities(self.alg.getEntities())

            # Only after move animation is done, the new entity positions are calculated
            if move_done:
                self.alg.removeEdgesFromTile()
                self.alg.update()
                self.alg.evaporate()



            pygame.display.flip()
