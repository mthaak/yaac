import sys

from pygame.constants import *
from pygame.key import *

from src.alg.ACO import Entity
from src.gui.HUD import HUD, HUDMode
from src.gui.Renderer import Renderer
from src.gui.lamina.lamina import *
from src.map.Map import Prop


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
        self.screen_width, self.screen_height = 1920, 1080
        viewport = (self.screen_width, self.screen_height)
        srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF | FULLSCREEN)
        pygame.display.set_caption('YAAC')
        self.clock = pygame.time.Clock()

        self.renderer = Renderer(viewport, map, alg)
        self.hud = HUD(viewport, map, alg)
        self.hud_ticks = 500  # refresh time for hud
        self.hud_refreshed = False

        self.moving_prop = False  # whether a prop is being moved

        self.hud.refresh()  # first draw

        self.map.__init__()
        self.alg.__init__(self.map)
        self.alg.update()  # first update needed to let entities get correct orientation

        self.mainloop()  # start main loop

    def mainloop(self):
        while 1:
            self.clock.tick()

            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()

                elif e.type == KEYDOWN and e.key == K_g:
                    self.renderer.toggleShowGrid()
                elif e.type == KEYDOWN and e.key == K_e:
                    self.renderer.toggleShowEdges()
                elif e.type == KEYDOWN and e.key == K_p:
                    self.map.print()
                elif e.type == KEYDOWN and e.key == K_COMMA:
                    if self.renderer.entity_move_frames > 1:
                        self.renderer.entity_move_frames -= 1
                        self.hud.updateMoveFrames(self.renderer.entity_move_frames)
                elif e.type == KEYDOWN and e.key == K_PERIOD:
                    self.renderer.entity_move_frames += 1
                    self.hud.updateMoveFrames(self.renderer.entity_move_frames)
                elif e.type == KEYDOWN and e.key == K_m:
                    self.map.toggleMap()
                    self.alg.__init__(self.map)  # reinitiate ACO
                elif e.type == KEYDOWN and e.key == K_n:
                    self.map.togglePreviousMap()
                    self.alg.__init__(self.map)

                # HUD mode select
                if e.type == KEYDOWN and e.key in [K_ESCAPE, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]:
                    self.renderer.selected_tile = None
                    self.renderer.move_prop = None
                    self.renderer.new_prop = None
                    self.renderer.old_prop = None
                    self.renderer.new_entity = None
                    self.moving_prop = False
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    self.hud.mode = HUDMode.NONE
                    self.hud.refresh()
                elif e.type == KEYDOWN and e.key == K_1:
                    self.hud.mode = HUDMode.TOGGLE
                    self.renderer.selected_tile = (-1, -1)
                    self.hud.refresh()
                elif e.type == KEYDOWN and e.key == K_2:
                    self.hud.mode = HUDMode.PLACE_RABBIT
                    self.renderer.new_entity = Entity.randomRabbit(self.map, self.alg, -1, -1)
                    self.hud.refresh()
                elif e.type == KEYDOWN and e.key == K_3:
                    self.hud.mode = HUDMode.PLACE_START
                    self.renderer.new_prop = Prop.randomHole(-1, -1)
                    self.hud.refresh()
                elif e.type == KEYDOWN and e.key == K_4:
                    self.hud.mode = HUDMode.PLACE_END
                    self.renderer.new_prop = Prop.randomFood(-1, -1)
                    self.hud.refresh()
                elif e.type == KEYDOWN and e.key == K_5:
                    self.hud.mode = HUDMode.PLACE_TREE
                    self.renderer.new_prop = Prop.randomTree(-1, -1)
                    self.hud.refresh()
                elif e.type == KEYDOWN and e.key == K_6:
                    self.hud.mode = HUDMode.PLACE_ROCK
                    self.renderer.new_prop = Prop.randomRock(-1, -1)
                    self.hud.refresh()
                elif e.type == KEYDOWN and e.key == K_7:
                    self.hud.mode = HUDMode.PLACE_DECORATION
                    self.renderer.new_prop = Prop.randomDecoration(-1, -1)
                    self.hud.refresh()
                elif e.type == KEYDOWN and e.key == K_8:
                    self.hud.mode = HUDMode.MOVE
                    self.renderer.move_prop = (-1, -1)
                    self.hud.refresh()
                elif e.type == KEYDOWN and e.key == K_9:
                    self.hud.mode = HUDMode.DELETE
                    self.hud.refresh()

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
                        elif self.hud.mode == HUDMode.PLACE_RABBIT:
                            tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                            if tile is not None and not self.map.tileOccupied(*tile):
                                self.alg.placeEntity(self.renderer.new_entity)
                                self.renderer.new_entity = Entity.randomRabbit(self.map, self.alg, -1, -1)
                        elif self.hud.mode == HUDMode.PLACE_START:
                            tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                            if tile is not None and not self.map.tileOccupied(*tile) and not self.alg.tileOccupied(
                                    *tile):
                                self.map.placeProp(self.renderer.new_prop)
                                self.map.addStartPos(*tile)
                                self.alg.fixEdgesHole(*tile, self.renderer.new_prop.r)
                                self.renderer.new_prop = Prop.randomHole(-1, -1)
                        elif self.hud.mode == HUDMode.PLACE_END:
                            tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                            if tile is not None and not self.map.tileOccupied(*tile) and not self.alg.tileOccupied(
                                    *tile):
                                self.map.placeProp(self.renderer.new_prop)
                                self.map.addEndPos(*tile)
                                self.renderer.new_prop = Prop.randomFood(-1, -1)
                        elif self.hud.mode == HUDMode.PLACE_TREE:
                            tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                            if tile is not None and not self.map.tileOccupied(*tile) and not self.alg.tileOccupied(
                                    *tile):
                                self.map.placeProp(self.renderer.new_prop)
                                self.alg.fixEdges(*tile)
                                self.renderer.new_prop = Prop.randomTree(-1, -1)
                        elif self.hud.mode == HUDMode.PLACE_ROCK:
                            tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                            if tile is not None and not self.map.tileOccupied(*tile) and not self.alg.tileOccupied(
                                    *tile):
                                self.map.placeProp(self.renderer.new_prop)
                                self.alg.fixEdges(*tile)
                                self.renderer.new_prop = Prop.randomRock(-1, -1)
                        elif self.hud.mode == HUDMode.PLACE_DECORATION:
                            tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                            if tile is not None and not self.map.tileOccupied(*tile) and not self.alg.tileOccupied(
                                    *tile):
                                self.map.placeProp(self.renderer.new_prop)
                                self.alg.fixEdges(*tile)
                                self.renderer.new_prop = Prop.randomDecoration(-1, -1)
                        elif self.hud.mode == HUDMode.MOVE:
                            if self.moving_prop:
                                tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                                if tile is not None and not self.map.tileOccupied(*tile) and not self.alg.tileOccupied(
                                        *tile):
                                    self.map.placeProp(self.renderer.move_prop)
                                    self.alg.fixEdges(*tile)
                                    self.renderer.move_prop = (-1, -1)
                                    self.moving_prop = False
                            else:
                                tile = self.renderer.getPropCoords(e.pos[0], e.pos[1])
                                if tile is None:
                                    tile = self.renderer.getTileCoords(e.pos[0], e.pos[1])
                                    if tile and self.map.getProp(*tile) is None:
                                        tile = None
                                if tile is not None:
                                    self.renderer.move_prop = self.map.getProp(*tile)
                                    self.map.removeProp(*tile)
                                    self.alg.fixEdges(*tile)
                                    self.moving_prop = True
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
                    self.renderer.selected_tile = tile
            elif self.hud.mode == HUDMode.PLACE_RABBIT:
                tile = self.renderer.getTileCoords(pos[0], pos[1])
                if tile is not None and not self.map.tileOccupied(*tile):
                    self.renderer.new_entity.i, self.renderer.new_entity.j = tile
                else:
                    self.renderer.new_entity.i, self.renderer.new_entity.j = (-1, -1)
            elif self.hud.mode == HUDMode.PLACE_START:
                tile = self.renderer.getTileCoords(pos[0], pos[1])
                if tile is not None and not self.map.tileOccupied(*tile) and not self.alg.tileOccupied(*tile):
                    self.renderer.new_prop.i, self.renderer.new_prop.j = tile
                else:
                    self.renderer.new_prop.i, self.renderer.new_prop.j = (-1, -1)
            elif self.hud.mode == HUDMode.PLACE_END:
                tile = self.renderer.getTileCoords(pos[0], pos[1])
                if tile is not None and not self.map.tileOccupied(*tile) and not self.alg.tileOccupied(*tile):
                    self.renderer.new_prop.i, self.renderer.new_prop.j = tile
                else:
                    self.renderer.new_prop.i, self.renderer.new_prop.j = (-1, -1)
            elif self.hud.mode == HUDMode.PLACE_TREE:
                tile = self.renderer.getTileCoords(pos[0], pos[1])
                if tile is not None and not self.map.tileOccupied(*tile) and not self.alg.tileOccupied(*tile):
                    self.renderer.new_prop.i, self.renderer.new_prop.j = tile
                else:
                    self.renderer.new_prop.i, self.renderer.new_prop.j = (-1, -1)
            elif self.hud.mode == HUDMode.PLACE_ROCK:
                tile = self.renderer.getTileCoords(pos[0], pos[1])
                if tile is not None and not self.map.tileOccupied(*tile) and not self.alg.tileOccupied(*tile):
                    self.renderer.new_prop.i, self.renderer.new_prop.j = tile
                else:
                    self.renderer.new_prop.i, self.renderer.new_prop.j = (-1, -1)
            elif self.hud.mode == HUDMode.PLACE_DECORATION:
                tile = self.renderer.getTileCoords(pos[0], pos[1])
                if tile is not None and not self.map.tileOccupied(*tile) and not self.alg.tileOccupied(*tile):
                    self.renderer.new_prop.i, self.renderer.new_prop.j = tile
                else:
                    self.renderer.new_prop.i, self.renderer.new_prop.j = (-1, -1)
            elif self.hud.mode == HUDMode.MOVE:
                if self.moving_prop:
                    tile = self.renderer.getTileCoords(pos[0], pos[1])
                    if tile is not None:
                        self.renderer.move_prop.i, self.renderer.move_prop.j = tile
                    else:
                        self.renderer.move_prop.i, self.renderer.move_prop.j = (-1, -1)
                else:
                    tile = self.renderer.getPropCoords(pos[0], pos[1])
                    if tile is None:
                        tile = self.renderer.getTileCoords(pos[0], pos[1])
                        if tile and self.map.getProp(*tile) is None:
                            tile = None
                    if tile is not None:
                        self.renderer.move_prop = (tile[0], tile[1])
                    else:
                        self.renderer.move_prop = None

            elif self.hud.mode == HUDMode.DELETE:
                tile = self.renderer.getPropCoords(pos[0], pos[1])
                if tile is None:
                    tile = self.renderer.getTileCoords(pos[0], pos[1])
                    if tile and self.map.getProp(*tile) is None:
                        tile = None
                if tile is not None:
                    self.renderer.old_prop = (tile[0], tile[1])
                else:
                    self.renderer.old_prop = None

            # Render
            ticks = pygame.time.get_ticks()
            self.renderer.render()
            # print('render map -', pygame.time.get_ticks() - ticks)

            move_done = self.renderer.isAnimationDone()
            # print('render entities -', pygame.time.get_ticks() - ticks)

            # Only after move animation is done, the new entity positions are calculated
            if move_done:
                ticks = pygame.time.get_ticks()
                self.alg.update()
                self.alg.evaporate()
                # print('alg -', pygame.time.get_ticks() - ticks)

            if pygame.time.get_ticks() % 1000 < self.hud_ticks:
                if not self.hud_refreshed:
                    ticks = pygame.time.get_ticks()
                    self.hud.updateFPS(self.clock.get_fps())
                    self.hud.refresh()
                    self.hud_refreshed = True
                    # print('hud -', pygame.time.get_ticks() - ticks)
            else:
                self.hud_refreshed = False

            self.renderer.renderHUD(self.hud.getSurface())
            pygame.display.flip()
