from enum import Enum

import pygame

from src.gui.lamina.lamina import LaminaScreenSurface


class HUD:
    def __init__(self, viewport, map, alg):
        self.viewport = viewport
        self.map = map
        self.alg = alg

        self.screen = LaminaScreenSurface(0.985)

        self.mode = HUDMode.NONE

        self.fps = 60
        self.move_frames = 10

    def refresh(self):
        self.screen.clear()

        modes_x, modes_y, modes_line_height = 10, 10, 30
        square_size = 15
        font = pygame.font.Font(None, 20)
        big_font = pygame.font.Font(None, 28)

        txt = big_font.render('Modes', 1, (0, 0, 0))
        self.screen.surf.blit(txt, (modes_x, modes_y))

        text = [
            'None',
            'Toggle tiles (1)',
            'Place rabbit (2)',
            'Place hole (3)',
            'Place food (4)',
            'Place tree (5)',
            'Place rock (6)',
            'Place decoration (7)',
            'Move (8)',
            'Delete (9)'
        ]
        for i in range(1, 10):
            txt = font.render(text[i], 1, (0, 0, 0))
            self.screen.surf.blit(txt, (modes_x + square_size + 5, modes_y + i * modes_line_height + 2))
            square = [(modes_x, modes_y + i * modes_line_height + square_size),
                      (modes_x, modes_y + i * modes_line_height),
                      (modes_x + square_size, modes_y + i * modes_line_height),
                      (modes_x + square_size, modes_y + i * modes_line_height + square_size)]
            if self.mode.value == i:
                pygame.draw.polygon(self.screen.surf, (0, 0, 0), square, 0)
            else:
                pygame.draw.polygon(self.screen.surf, (0, 0, 0), square, 2)

        txt = big_font.render('Other hotkeys', 1, (0, 0, 0))
        self.screen.surf.blit(txt, (200, 10))
        txt = font.render('Show grid (g)', 1, (0, 0, 0))
        self.screen.surf.blit(txt, (200, 40))
        txt = font.render('Show edges (e)', 1, (0, 0, 0))
        self.screen.surf.blit(txt, (200, 70))
        txt = font.render('Print map in console (p)', 1, (0, 0, 0))
        self.screen.surf.blit(txt, (200, 100))
        txt = font.render('Toggle between maps (m)', 1, (0, 0, 0))
        self.screen.surf.blit(txt, (200, 130))

        txt = font.render('Number of rabbits: ' + str(len(self.alg.getEntities())), 1, (0, 0, 0))
        self.screen.surf.blit(txt, (self.viewport[0] - 180, 10))
        txt = font.render('Best path: ' + str(self.alg.getBestPath()), 1, (0, 0, 0))
        self.screen.surf.blit(txt, (self.viewport[0] - 180, 40))
        txt = font.render('FPS: ' + str(round(self.fps, 2)), 1, (0, 0, 0))
        self.screen.surf.blit(txt, (self.viewport[0] - 180, 70))
        txt = font.render('Move frames (,.): ' + str(self.move_frames), 1, (0, 0, 0))
        self.screen.surf.blit(txt, (self.viewport[0] - 180, 100))

        self.screen.refresh()
        # self.screen.refreshPosition()

    def getSurface(self):
        return self.screen

    def updateFPS(self, fps):
        self.fps = fps

    def updateMoveFrames(self, move_frames):
        self.move_frames = move_frames


class HUDMode(Enum):
    NONE = 0  # (Esc)
    TOGGLE = 1  # (T)
    PLACE_RABBIT = 2  # (B)
    PLACE_START = 3  # (H)
    PLACE_END = 4  # (F)
    PLACE_TREE = 5  # (T)
    PLACE_ROCK = 6  # (R)
    PLACE_DECORATION = 7  # (D)
    MOVE = 8  # (M)
    DELETE = 9  # (D)
