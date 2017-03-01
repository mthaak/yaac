import pygame
import sys

from pygame.constants import *
from pygame.key import *

from src.gui.Renderer import Renderer


class GUI:
    def __init__(self, map, alg):
        self.map = map
        self.alg = alg

        # Set up Pygame
        pygame.init()
        viewport = (800, 600)
        hx = viewport[0] / 2
        hy = viewport[1] / 2
        srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
        self.clock = pygame.time.Clock()

        # Set up renderer
        self.renderer = Renderer()

        # Set view
        self.renderer.setView(viewport)

        # Set view parameters
        self.phi, self.theta = 90, 350
        self.zpos = 15
        self.renderer.setOrbit(self.phi, self.theta)
        self.renderer.setZoom(self.zpos)

        self.select = None

        self.mainloop()  # start main loop

    def mainloop(self):
        while 1:
            self.clock.tick(30)
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()
                elif e.type == KEYDOWN and e.key == K_ESCAPE:
                    sys.exit()
                elif e.type == MOUSEBUTTONDOWN:
                    if e.button == 4:
                        self.zpos = max(1, self.zpos - 1)
                        self.renderer.setZoom(self.zpos)
                    elif e.button == 5:
                        self.zpos += 1
                        self.renderer.setZoom(self.zpos)
                    elif e.button == 1:
                        self.select = self.renderer.getTileCoords(self.map, e.pos[0], e.pos[1])
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

            # Update alg
            changed = self.alg.update()
            entities = self.alg.getEntities()


            # Render
            self.renderer.renderMap(self.map, select=self.select)
            self.renderer.renderEntities(entities)

            pygame.display.flip()
