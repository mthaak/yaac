import math
import os

import numpy
from OpenGL.GLU import *

from src.gui.objloader import *
from src.map.Map import *


class TileModel(Enum):
    FLAT_DIRT = 1
    RIVER_STRAIGHT_DIRT = 2
    DECLINE_DIRT = 3
    INCLINE_DIRT = 4
    RIVER_CORNER_DIRT = 91
    CLIFF_TOP_CORNER_DIRT = 115
    CLIFF_TOP_WATERFALL_DIRT = 125
    CLIFF_TOP_DIRT = 127
    RIVER_END_DIRT = 145
    RIVER_TJUNCTION_DIRT = 146
    RIVER_JUNCTION_DIRT = 147


class Renderer:
    def __init__(self, map):
        self.map = map

        width, height = map.getSize()
        self.center_x = width / 2 * 3
        self.center_y = height / 2 * -3
        self.phi, self.theta = 0, 350  # used for camera position
        self.zpos = 15  # camera zoom

        self.background = self._texFromPNG('res/background.png')

        tile_model_ids = [TileModel.FLAT_DIRT,
                          TileModel.RIVER_STRAIGHT_DIRT,
                          TileModel.DECLINE_DIRT,
                          TileModel.INCLINE_DIRT,
                          TileModel.RIVER_CORNER_DIRT,
                          TileModel.CLIFF_TOP_CORNER_DIRT,
                          TileModel.CLIFF_TOP_WATERFALL_DIRT,
                          TileModel.CLIFF_TOP_DIRT,
                          TileModel.RIVER_END_DIRT,
                          TileModel.RIVER_TJUNCTION_DIRT,
                          TileModel.RIVER_JUNCTION_DIRT]

        # Load tile models
        os.chdir('../res/naturepack_extended/Models/')  # to prevent file path problems
        self.tile_models = {}
        self.tile_models_mono = {}  # monocolored tiles
        for tile_model_id in tile_model_ids:
            path = 'naturePack_{0:03d}.obj'.format(tile_model_id.value)
            self.tile_models[tile_model_id] = OBJ(path, swapyz=True)
            self.tile_models_mono[tile_model_id] = OBJ(path, swapyz=True, monocolor=True)
        os.chdir('../../../src')  # change back

        # Load point models
        os.chdir('../res/')
        self.rabbit_hole_model = OBJ('rabbit_hole.obj', swapyz=True)
        os.chdir('../src')
        os.chdir('../res/naturepack_extended/Models/')
        self.rabbit_food_model = OBJ('naturePack_flat_005.obj', swapyz=True)
        os.chdir('../../../src')

        # Prepare grid
        self.grid = self._prepareGrid()

        # Load entity models
        os.chdir('../res/rabbit/anim_run')
        self.rabbit_models = []
        self.rabbit_anim_frame = 0
        self.rabbit_anim_frames = 3
        self.rabbit_anim_counter = 0
        self.rabbit_anim_frame_length = 1
        for frame in range(self.rabbit_anim_frames):
            self.rabbit_models.append(OBJ('rabbit_{0:06d}.obj'.format(frame), swapyz=True, monocolor=True))
        os.chdir('../../../src')

        self.entity_move_frame = 0
        self.entity_move_frames = 15

        # Initialise OpenGL settings
        glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded

    def renderMap(self, select=None, show_grid=False):
        """Renders the complete map."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor(1.0, 1.0, 1.0)
        glBindTexture(GL_TEXTURE_2D, 0)  # unbind previous texture

        self._renderBackground()

        self._resetCamera()

        self._renderTiles(select=select)

        self._resetCamera()

        self._renderPoints()

        if show_grid:
            self._resetCamera()
            glCallList(self.grid)  # render grid

    def renderEntities(self, entities):
        """Renders all the entities."""
        self._resetCamera()

        scale = 0.05
        dev_x, dev_y = 1.5, -1
        for i, entity in enumerate(entities):
            glTranslate(3 * entity.i, -3 * entity.j, 0.25)
            glRotate(-entity.orient, 0, 0, 1)

            if entity.orient == 90 or entity.orient == 180:
                glTranslate(0, 3, 0)
            if entity.orient == 180 or entity.orient == 270:
                glTranslate(-3, 0, 0)

            glTranslate(dev_x, dev_y - 3 + self.entity_move_frame / self.entity_move_frames * 3, 0)

            glScale(scale, scale, scale)
            # Give the rabbits a different color
            if i == 0:
                glColor(1.0, 1.0, 1.0)
            elif i == 1:
                glColor(0.1, 0.1, 0.1)
            elif i == 2:
                glColor(0.40, 0.27, 0.20)
            glCallList(self.rabbit_models[self.rabbit_anim_frame].gl_list)
            glScale(1 / scale, 1 / scale, 1 / scale)

            glTranslate(-dev_x, -dev_y + 3 - self.entity_move_frame / self.entity_move_frames * 3, 0)

            if entity.orient == 90 or entity.orient == 180:
                glTranslate(0, -3, 0)
            if entity.orient == 180 or entity.orient == 270:
                glTranslate(3, 0, 0)

            glRotate(entity.orient, 0, 0, 1)
            glTranslate(-3 * entity.i, 3 * entity.j, -0.25)

        self.rabbit_anim_counter += 1
        if self.rabbit_anim_counter > self.rabbit_anim_frame_length:
            self.rabbit_anim_frame = (self.rabbit_anim_frame + 1) % self.rabbit_anim_frames
            self.rabbit_anim_counter = 0

        self.entity_move_frame = (self.entity_move_frame + 1) % self.entity_move_frames

        return self.entity_move_frame == 0

    def setOrbit(self, phi, theta):
        self.phi, self.theta = phi, theta

    def setZoom(self, zpos):
        self.zpos = zpos

    def getTileCoords(self, x, y, screen_height):
        """Gets the tile coordinates (i,j) for the tile under screen coordinates x, y."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self._resetCamera()
        self._renderTiles(self.map, pick=True)
        color = tuple(glReadPixels(x, screen_height - y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE))
        if color in list(self.colorToTile.keys()):
            return self.colorToTile[color]
        else:  # tile not found
            return None

    def _setView(self, viewport):
        """Sets initial view settings."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width, height = viewport
        gluPerspective(90.0, width / float(height), 1, 100.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)

    def _resetCamera(self):
        """Sets the view such that it looks at the center of the map from the sky."""
        glLoadIdentity()
        self.center_x = 5.5 * 3
        self.center_y = -4 * 3
        self.center_z = 0
        to_rad = (math.pi / 180)
        cam_x = self.center_x + self.zpos * math.cos(self.phi * to_rad) * math.sin(self.theta * to_rad)
        cam_y = self.center_y + self.zpos * math.sin(self.phi * to_rad) * math.sin(self.theta * to_rad)
        eye_z = self.center_z + self.zpos * math.cos(self.theta * to_rad)
        # Set the camera position and look at point
        gluLookAt(cam_x, cam_y, eye_z,  # camera position
                  self.center_x, self.center_y, self.center_z,  # look at point
                  0.0, 0.0, 1.0)  # up vector

    def _renderBackground(self):
        """Renders the background."""
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.background)

        glNormal3f(0.0, 0.0, 1.0)  # reset normal

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(-1.0, -1.0)
        glTexCoord2f(1, 0)
        glVertex2f(1.0, -1.0)
        glTexCoord2f(1, 1)
        glVertex2f(1.0, 1.0)
        glTexCoord2f(0, 1)
        glVertex2f(-1.0, 1.0)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

    def _renderTiles(self, select=None, pick=False):
        """Renders the tiles.
        :type select: tuple (i,j), the selected tile
        :type pick: boolean, whether a tile was picked so that every tile should get a different color
        """
        if pick:
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_LIGHTING)
            self.colorToTile = {}

        width, height = self.map.getSize()
        for j in range(height):
            for i in range(width):
                # Determine tile model id and orientation
                model_id, orientation = self._getTile(i, j)
                glRotate(-orientation, 0, 0, 1)
                if orientation == 90 or orientation == 180:
                    glTranslate(0, 3, 0)
                if orientation == 180 or orientation == 270:
                    glTranslate(-3, 0, 0)

                if model_id == TileModel.CLIFF_TOP_DIRT \
                        or model_id == TileModel.CLIFF_TOP_WATERFALL_DIRT:  # the cliff edges have a deviation
                    glTranslate(2.5, 0, 0.01)

                if model_id == TileModel.CLIFF_TOP_CORNER_DIRT:  # the cliff corners have a deviation as well
                    glTranslate(2.08, 0, 0.01)

                if pick:
                    color = (int(i / width * 255), int(j / height * 255), 255)
                    glColor3ub(*color)
                    self.colorToTile[color] = (i, j)
                    glCallList(self.tile_models_mono[model_id].gl_list)  # draw mono tile model
                elif select == (i, j):
                    glDisable(GL_LIGHTING)  # so that tile gets a slightly different shade (depends on angle though)
                    glCallList(self.tile_models[model_id].gl_list)  # draw tile model
                    glEnable(GL_LIGHTING)
                else:
                    glCallList(self.tile_models[model_id].gl_list)  # draw tile model

                if model_id == TileModel.CLIFF_TOP_DIRT \
                        or model_id == TileModel.CLIFF_TOP_WATERFALL_DIRT:  # the edges have a deviation
                    glTranslate(-2.5, 0, -0.01)

                if model_id == TileModel.CLIFF_TOP_CORNER_DIRT:  # the cliff corners have a deviation as well
                    glTranslate(-2.08, 0, -0.01)

                if orientation == 90 or orientation == 180:
                    glTranslate(0, -3, 0)
                if orientation == 180 or orientation == 270:
                    glTranslate(3, 0, 0)
                glRotate(orientation, 0, 0, 1)

                glTranslate(3, 0, 0)
            glTranslate(-3 * width, -3, 0)

        if pick:
            glEnable(GL_LIGHTING)
            glEnable(GL_TEXTURE_2D)

    def _renderPoints(self):
        """Renders the start and end points."""
        points = [self.map.getStartPos(), self.map.getEndPos()]
        scale = 1.0
        for i, point in enumerate(points):
            dev_x, dev_y = 0, 0
            orient = 0
            if i == 0:
                orient = 90
            if i == 1:
                dev_x, dev_y = 1, -1

            glTranslate(3 * point[0], -3 * point[1], 0.25)

            glRotate(-orient, 0, 0, 1)
            if orient == 90 or orient == 180:
                glTranslate(0, 3, 0)
            if orient == 180 or orient == 270:
                glTranslate(-3, 0, 0)

            glTranslate(dev_x, dev_y, 0)

            glScale(scale, scale, scale)
            if i == 0:
                glCallList(self.rabbit_hole_model.gl_list)
            elif i == 1:
                glCallList(self.rabbit_food_model.gl_list)
            glScale(1 / scale, 1 / scale, 1 / scale)

            glTranslate(-dev_x, -dev_y, 0)

            if orient == 90 or orient == 180:
                glTranslate(0, -3, 0)
            if orient == 180 or orient == 270:
                glTranslate(3, 0, 0)
            glRotate(orient, 0, 0, 1)

            glTranslate(-3 * point[0], 3 * point[1], -0.25)

    def _prepareGrid(self):
        """Prepares a display list for the grid."""
        # Load textures for characters
        chars = '0123456789,'
        # chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' \
        #         '0123456789 !@#$%^&*()-=_+\|[]{};:\'",.<>/?`~'
        char_textures = {}
        for char in chars:
            char_textures[char] = self._charTexFromPNG(char)

            # Create display list
        dplist = glGenLists(1)
        glNewList(dplist, GL_COMPILE)

        glLineWidth(1.0)
        glColor3f(1.0, 0.0, 0.0)
        x_dev, y_dev = 2.3, 2.3

        width, height = self.map.getSize()

        # Draw grid
        glBegin(GL_LINES)
        for i in range(1, width):
            glVertex3f(3 * i, -y_dev, 0.32)
            glVertex3f(3 * i, -3 * height + y_dev, 0.32)
        for j in range(1, height):
            glVertex3f(x_dev, -3 * j, 0.32)
            glVertex3f(3 * width - x_dev, -3 * j, 0.32)
        glEnd()

        glColor(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Draw coordinates of grid cells
        char_width, char_height, margin = 0.6, 0.6, 0.1
        for i in range(0, width):
            for j in range(0, height):
                string = '{0},{1}'.format(i, j)
                for k, c in enumerate(string):
                    glBindTexture(GL_TEXTURE_2D, char_textures[c])
                    glBegin(GL_QUADS)
                    glTexCoord2f(0, 0)
                    glVertex3f(3 * i + margin + char_width * k, -3 * j - margin, 0.32)
                    glTexCoord2f(1, 0)
                    glVertex3f(3 * i + margin + char_width + char_width * k, -3 * j - margin, 0.32)
                    glTexCoord2f(1, 1)
                    glVertex3f(3 * i + margin + char_width + char_width * k, -3 * j - margin - char_height, 0.32)
                    glTexCoord2f(0, 1)
                    glVertex3f(3 * i + margin + char_width * k, -3 * j - margin - char_height, 0.32)
                    glEnd()

        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)

        glEndList()
        return dplist

    def _getTile(self, i, j):
        """Determines model id and orientation for some tile."""
        tiles = self.map.getTiles()
        width, height = self.map.getSize()
        model_id, orientation = 0, 0
        if ((i == 0 or i == width - 1) and not (j == 0 or j == height - 1)) \
                or ((j == 0 or j == height - 1) and not (i == 0 or i == width - 1)):
            if tiles[i][j] == Tile.LAND.value:
                model_id = TileModel.CLIFF_TOP_DIRT
            elif tiles[i][j] == Tile.WATER.value:
                model_id = TileModel.CLIFF_TOP_WATERFALL_DIRT
            if i == 0:
                orientation = 0
            elif j == 0:
                orientation = 90
            elif i == width - 1:
                orientation = 180
            elif j == height - 1:
                orientation = 270

        elif (i == 0 or i == width - 1) and (j == 0 or j == height - 1):
            model_id = TileModel.CLIFF_TOP_CORNER_DIRT
            if i == 0 and j == 0:
                orientation = 90
            elif i == 0 and j == height - 1:
                orientation = 0
            elif i == width - 1 and j == 0:
                orientation = 180
            elif i == width - 1 and j == height - 1:
                orientation = 270
        else:
            if tiles[i][j] == Tile.LAND.value:
                model_id = TileModel.FLAT_DIRT
            elif tiles[i][j] == Tile.WATER.value:
                neighbours = tiles[i][j - 1], tiles[i + 1][j], tiles[i][j + 1], tiles[i - 1][j]  # n, e, s, w
                if neighbours == (0, 0, 0, 0):
                    model_id = TileModel.RIVER_END_DIRT  # TODO create water pool
                elif neighbours == (1, 0, 0, 0):
                    model_id = TileModel.RIVER_END_DIRT
                    orientation = 0
                elif neighbours == (0, 1, 0, 0):
                    model_id = TileModel.RIVER_END_DIRT
                    orientation = 90
                elif neighbours == (0, 0, 1, 0):
                    model_id = TileModel.RIVER_END_DIRT
                    orientation = 180
                elif neighbours == (0, 0, 0, 1):
                    model_id = TileModel.RIVER_END_DIRT
                    orientation = 270
                elif neighbours == (1, 0, 1, 0):
                    model_id = TileModel.RIVER_STRAIGHT_DIRT
                elif neighbours == (0, 1, 0, 1):
                    model_id = TileModel.RIVER_STRAIGHT_DIRT
                    orientation = 90
                elif neighbours == (1, 1, 0, 0):
                    model_id = TileModel.RIVER_CORNER_DIRT
                    orientation = 180
                elif neighbours == (0, 1, 1, 0):
                    model_id = TileModel.RIVER_CORNER_DIRT
                    orientation = 270
                elif neighbours == (0, 0, 1, 1):
                    model_id = TileModel.RIVER_CORNER_DIRT
                    orientation = 0
                elif neighbours == (1, 0, 0, 1):
                    model_id = TileModel.RIVER_CORNER_DIRT
                    orientation = 90
                elif neighbours == (1, 1, 1, 0):
                    model_id = TileModel.RIVER_TJUNCTION_DIRT
                    orientation = 180
                elif neighbours == (0, 1, 1, 1):
                    model_id = TileModel.RIVER_TJUNCTION_DIRT
                    orientation = 270
                elif neighbours == (1, 0, 1, 1):
                    model_id = TileModel.RIVER_TJUNCTION_DIRT
                    orientation = 0
                elif neighbours == (1, 1, 0, 1):
                    model_id = TileModel.RIVER_TJUNCTION_DIRT
                    orientation = 90
                elif neighbours == (1, 1, 1, 1):
                    model_id = TileModel.RIVER_JUNCTION_DIRT
        return model_id, orientation

    def _texFromPNG(self, filename):
        """Creates a texture from a PNG image."""
        img = pygame.image.load('../' + filename)
        img_data = numpy.array(list(img.get_view().raw), numpy.uint8)

        texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.get_size()[0], img.get_size()[1], 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     img_data)
        return texture

    def _charTexFromPNG(self, char):
        """Creates a texture of a text character from a image of characters."""
        # Draw coordinates
        os.chdir('gui/bmpfont')
        from src.gui.bmpfont.bmpfont import BmpFont
        bmpfont = BmpFont()
        img = pygame.image.load('font.png')
        os.chdir('../..')
        img_data = numpy.array(list(img.get_view().raw), numpy.uint8)

        width, height, chars_per_line = 8, 16, 8
        img_x, img_y = bmpfont.chartable[char]
        img_char = numpy.array([])  # pixels of character
        for y in range(img_y, img_y + height):
            img_char = numpy.append(img_char,
                                    img_data[4 * (y * chars_per_line * width + img_x):
                                    4 * (y * chars_per_line * width + img_x + width)])

        texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 8, 16, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     img_char)
        return texture
