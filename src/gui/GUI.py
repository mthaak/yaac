import sys

from pygame.constants import *
from pygame.key import *

from src.gui.HUD import HUD, HUDMode
from src.gui.Renderer import Renderer
from src.gui.lamina.lamina import *


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
        # start_pygame()

        pygame.init()
        self.screen_width, self.screen_height = 1280, 1024
        viewport = (self.screen_width, self.screen_height)
        srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
        pygame.display.set_caption('YAAC')
        self.clock = pygame.time.Clock()

        self.renderer = Renderer(viewport, map, alg)
        self.hud = HUD(viewport, map, alg)

        self.movingProp = False  # whether a prop is being moved

        self.hud.redraw()  # first draw

        self.alg.update()  # first update needed to let entities get correct orientation

        self.mainloop()  # start main loop

    def mainloop(self):
        while 1:
            self.clock.tick(3000)  # fix fps on 30 fps

            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()

                elif e.type == KEYDOWN and e.key == K_g:
                    self.renderer.show_grid = not self.renderer.show_grid
                elif e.type == KEYDOWN and e.key == K_e:
                    self.renderer.show_edges = not self.renderer.show_edges

                # HUD mode select
                if e.type == KEYDOWN and e.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]:
                    self.renderer.selectedTile = None
                    self.renderer.moveProp = None
                    self.renderer.newProp = None
                    self.renderer.oldProp = None
                    self.movingProp = False
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    self.hud.mode = HUDMode.NONE
                    self.hud.redraw()
                elif e.type == KEYDOWN and e.key == K_1:
                    self.hud.mode = HUDMode.TOGGLE
                    self.renderer.selectedTile = (-1, -1)
                    self.hud.redraw()
                elif e.type == KEYDOWN and e.key == K_2:
                    self.hud.mode = HUDMode.PLACE_BUNNY
                    self.renderer.newProp = None  # TODO
                    self.hud.redraw()
                elif e.type == KEYDOWN and e.key == K_3:
                    self.hud.mode = HUDMode.PLACE_START
                    self.renderer.newProp = None  # TODO
                    self.hud.redraw()
                elif e.type == KEYDOWN and e.key == K_4:
                    self.hud.mode = HUDMode.PLACE_END
                    self.renderer.newProp = self.map.randomFood(-1, -1)
                    self.hud.redraw()
                elif e.type == KEYDOWN and e.key == K_5:
                    self.hud.mode = HUDMode.PLACE_TREE
                    self.renderer.newProp = self.map.randomTree(-1, -1)
                    self.hud.redraw()
                elif e.type == KEYDOWN and e.key == K_6:
                    self.hud.mode = HUDMode.PLACE_ROCK
                    self.renderer.newProp = self.map.randomRock(-1, -1)
                    self.hud.redraw()
                elif e.type == KEYDOWN and e.key == K_7:
                    self.hud.mode = HUDMode.PLACE_DECORATION
                    self.renderer.newProp = self.map.randomDecoration(-1, -1)
                    self.hud.redraw()
                elif e.type == KEYDOWN and e.key == K_8:
                    self.hud.mode = HUDMode.MOVE
                    self.renderer.moveProp = (-1, -1)
                    self.hud.redraw()
                elif e.type == KEYDOWN and e.key == K_9:
                    self.hud.mode = HUDMode.DELETE
                    self.hud.redraw()

                # Mouse events
                elif e.type == MOUSEBUTTONDOWN:
                    if e.button == 4:
                        self.renderer.zpos = max(9, self.renderer.zpos - 1)
                    elif e.button == 5:
                        self.renderer.zpos = min(50, self.renderer.zpos + 1)
                    elif e.button == 1:
                        if self.hud.mode == HUDMode.TOGGLE:
                            tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                            if tile is not None:
                                self.map.toggleTile(*tile)
                                self.alg.fixEdges(*tile)  # add/remove edges
                        elif self.hud.mode == HUDMode.PLACE_START:
                            tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                            if tile is not None and not self.map.tileOccupied(*tile):
                                pass  # TODO
                        elif self.hud.mode == HUDMode.PLACE_END:
                            tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                            if tile is not None and not self.map.tileOccupied(*tile):
                                self.map.placeProp(self.renderer.newProp)
                                self.map.addEndPos(*tile)
                                self.alg.fixEdges(*tile)
                                self.renderer.newProp = self.map.randomFood(-1, -1)
                        elif self.hud.mode == HUDMode.PLACE_TREE:
                            tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                            if tile is not None and not self.map.tileOccupied(*tile):
                                self.map.placeProp(self.renderer.newProp)
                                self.alg.fixEdges(*tile)
                                self.renderer.newProp = self.map.randomTree(-1, -1)
                        elif self.hud.mode == HUDMode.PLACE_ROCK:
                            tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                            if tile is not None and not self.map.tileOccupied(*tile):
                                self.map.placeProp(self.renderer.newProp)
                                self.alg.fixEdges(*tile)
                                self.renderer.newProp = self.map.randomRock(-1, -1)
                        elif self.hud.mode == HUDMode.PLACE_DECORATION:
                            tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                            if tile is not None and not self.map.tileOccupied(*tile):
                                self.map.placeProp(self.renderer.newProp)
                                self.alg.fixEdges(*tile)
                                self.renderer.newProp = self.map.randomDecoration(-1, -1)
                        elif self.hud.mode == HUDMode.MOVE:
                            if self.movingProp:
                                tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                                if tile is not None and not self.map.tileOccupied(*tile):
                                    self.map.placeProp(self.renderer.moveProp)
                                    self.alg.fixEdges(*tile)
                                    self.renderer.moveProp = (-1, -1)
                                    self.movingProp = False
                            else:
                                tile = self.renderer.getPropCoords(e.pos[0], e.pos[1])
                                if tile is None:
                                    tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                                    if tile and self.map.getProp(*tile) is None:
                                        tile = None
                                if tile is not None:
                                    self.renderer.moveProp = self.map.getProp(*tile)
                                    self.map.removeProp(*tile)
                                    self.alg.fixEdges(*tile)
                                    self.movingProp = True
                        elif self.hud.mode == HUDMode.DELETE:
                            tile = self.renderer.getPropCoords(e.pos[0], e.pos[1])
                            if tile is None:
                                tile = self.renderer.getTileCoords(pos[0], pos[1])
                                if tile and self.map.getProp(*tile) is None:
                                    tile = None
                            if tile is not None:
                                self.map.removeProp(*tile)
                                self.alg.fixEdges(*tile)

            # Update camera settings with arrow keys
            if get_pressed()[K_LEFT]:
                self.renderer.phi -= 5
            if get_pressed()[K_RIGHT]:
                self.renderer.phi += 5
            if get_pressed()[K_DOWN] and self.renderer.theta >= 280 + 5:
                self.renderer.theta -= 5
            if get_pressed()[K_UP] and self.renderer.theta <= 350 - 5:
                self.renderer.theta += 5

            # Selection by hovering
            pos = pygame.mouse.get_pos()
            if self.hud.mode == HUDMode.TOGGLE:
                tile = self.renderer.getTileCoords(pos[0], pos[1])
                if tile is not None:
                    self.renderer.selectedTile = tile
            elif self.hud.mode == HUDMode.PLACE_START:
                tile = self.renderer.getTileCoords(pos[0], pos[1])
                if tile is not None and not self.map.tileOccupied(*tile):
                    pass  # TODO
            elif self.hud.mode == HUDMode.PLACE_END:
                tile = self.renderer.getTileCoords(pos[0], pos[1])
                if tile is not None and not self.map.tileOccupied(*tile):
                    self.renderer.newProp.i, self.renderer.newProp.j = tile
                else:
                    self.renderer.newProp.i, self.renderer.newProp.j = (-1, -1)
            elif self.hud.mode == HUDMode.PLACE_TREE:
                tile = self.renderer.getTileCoords(pos[0], pos[1])
                if tile is not None and not self.map.tileOccupied(*tile):
                    self.renderer.newProp.i, self.renderer.newProp.j = tile
                else:
                    self.renderer.newProp.i, self.renderer.newProp.j = (-1, -1)
            elif self.hud.mode == HUDMode.PLACE_ROCK:
                tile = self.renderer.getTileCoords(pos[0], pos[1])
                if tile is not None and not self.map.tileOccupied(*tile):
                    self.renderer.newProp.i, self.renderer.newProp.j = tile
                else:
                    self.renderer.newProp.i, self.renderer.newProp.j = (-1, -1)
            elif self.hud.mode == HUDMode.PLACE_DECORATION:
                tile = self.renderer.getTileCoords(pos[0], pos[1])
                if tile is not None and not self.map.tileOccupied(*tile):
                    self.renderer.newProp.i, self.renderer.newProp.j = tile
                else:
                    self.renderer.newProp.i, self.renderer.newProp.j = (-1, -1)
            elif self.hud.mode == HUDMode.MOVE:
                if self.movingProp:
                    tile = self.renderer.getTileCoords(pos[0], pos[1])
                    if tile is not None:
                        self.renderer.moveProp.i, self.renderer.moveProp.j = tile
                    else:
                        self.renderer.moveProp.i, self.renderer.moveProp.j = (-1, -1)
                else:
                    tile = self.renderer.getPropCoords(pos[0], pos[1])
                    if tile is None:
                        tile = self.renderer.getTileCoords(pos[0], pos[1])
                        if tile and self.map.getProp(*tile) is None:
                            tile = None
                    if tile is not None:
                        self.renderer.moveProp = (tile[0], tile[1])
                    else:
                        self.renderer.moveProp = None

            elif self.hud.mode == HUDMode.DELETE:
                tile = self.renderer.getPropCoords(pos[0], pos[1])
                if tile is None:
                    tile = self.renderer.getTileCoords(pos[0], pos[1])
                    if tile and self.map.getProp(*tile) is None:
                        tile = None
                if tile is not None:
                    self.renderer.oldProp = (tile[0], tile[1])
                else:
                    self.renderer.oldProp = None

            # Render
            self.renderer.renderMap()
            move_done = self.renderer.renderEntities(self.alg.getEntities())

            # Only after move animation is done, the new entity positions are calculated
            if move_done:
                self.alg.update()
                self.alg.evaporate()

            self.renderer.renderHUD(self.hud.getSurface())
            pygame.display.flip()
